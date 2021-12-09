# Table of contents

* [Introduction](#introduction)
* [The big picture](#the-big-picture)
  * [Resources](#resources)
  * [CompositeResources](#compositeresources)
  * [Facade](#facade)
  * [Putting all this together](#Putting-all-this-together)
* [AWS](#aws)
  * [Regions](#regions)
  * [VPCs](#vpcs)
* [Azure](#azure)
* [GCP](#gcp)

# Introduction
One important component of Scout Suite is the resource configurations fetcher. The rule system is based entirely on analyzing those configurations. This article aims to be a comprehensive documentation of that component's architecture. The first section will discuss the architecture shared between the providers. The three subsequent sections will address the provider-specific architecture, respectively for Amazon Web Services (AWS), Azure and Google Cloud Platform (GCP).

# The big picture

First of all, it is important to know that the architecture is loosely based on the [composite pattern](https://sourcemaking.com/design_patterns/composite). We chose this pattern because a cloud infrastructure is a hierarchical structure. For example, for AWS, you have regions, which have virtual private networks (VPCs), which have virtual machines, which have volumes, and so on. There are two main classes you should know about: `Resources` and `CompositeResources`. The following UML diagram shows the relationship between `Resources` and `CompositeResources`.

<p align="center">
    <img align="center" src="https://i.imgur.com/84hKP8x.png" alt="Resources and CompositeResources UML" width="450px"/>
</p>

## Resources
`Resources` is the base class of the hierarchical structure. Everything is basically `Resources`. This `Resources` class inherits from the `dict` class. Instances of a given type of resources are stored within the internal dictionary, with instance ids as keys and instance configurations (which may store other nested resources) as values.

The resources **should not** communicate directly with the cloud service libraries. Instead, the resources should fetch the relevant data through a single call to the facade. The logic of aggregating the data from multiple calls to the API should be encapsulated in the facade, and the data parsing should be encapsulated in the resource class. 

## CompositeResources
`CompositeResources` represents a node in the hierarchical structure. As inherited from `Resources`, it may still store instances of a given type of resources internally, but also stores some kind of nested resources referred to as its 'children'.

Classes extending `CompositeResources` should define a `_children` attribute which consists of a list of tuples describing the children. The tuples are expected to respect the following format: (<child_class>, <child_name>). The child_name is used to indicate the name under which the child will be stored in the parent object. Although, you may use `None` to indicate that you want to store the content of a child directly into the parent (like there was no nesting at all). This is useful for some edge cases.

## Facade

`Resources` and `CompositeResources` communicate with their provider API through a facade. The methods should be scoped by services. For example, this means all the methods related to _EC2_ should be under the [`EC2Facade`](https://github.com/nccgroup/ScoutSuite/blob/refactoring/resource-configs/ScoutSuite/providers/aws/facade/ec2.py). 

Also, it is important to reduce the number of API calls done in order to prevent being throttled by the cloud provider involved. In order to do so, it is sometimes wise to cache some data. For example, some resources are categorized by VPC, but the API does not allow to specify a VPC, so it returns data for a whole region. If we were to make an API call for each VPC, we would pull the same data multiple times. Instead, we cache the whole region the first time we make the call.

## Putting all this together
Every provider should have its own implementation of `Resources` and `CompositeResources`. The `Resources` implementation could technically be empty, and that's fine. We added this layer of separation to prevent having the topmost classes polluted with provider-specific alternatives.

Let's look at a fictional provider called *Super Cloud Services* (SCC). Here's a bit of info about our imaginary provider:
* It has a service called `Super Cloud Computers`
* Resources are scoped by `Server Centers`
* `Super Cloud Computers` are scoped by `Virtual Private Network`
* `Super Cloud Computers` each have `Images` and `Volumes`
* `Server Centers` and `VPCs` could have other resources

Our structure would look like that:

<p align="center">
    <img align="center" src="https://i.imgur.com/rRhljna.png" alt="Resources and CompositeResources UML" width="550px"/>
</p>


Here are a few comments on the diagram above:
* We have specializations of both `Resources` and `CompositeResources`: `SCSResources` and `SCSCompositeResources`
* `ServerCenter` implements `SCSCompositeResource`. It is an abstract class which takes care of fetching all the server centers, and then fetches children in each server center
* `SuperCloudComputerService` inherits `ServerCenter` and registers `VPCS` in the children attribute.
* `VPCS` is a composite and has `SuperCloudComputer` in its children attribute
* `SuperCloudComputer` is also a composite and has `Snapshots` and `Volumes` in its children attribute
* `Snapshots` and `Volumes` are resources
* The facade is not displayed, but we can assume we have some kind of `SCSFacade`, and the resources communicate with it to fetch the resources

# AWS

AWS has two implementations of `CompositeResources` you may use to simplify the implementation of new services: `Regions` and `Vpcs`. 

## Regions

The `Regions` class hides one layer of the tree by fetching the services defined in `_children` in each region. See the implementation of [`AWSLambas`](https://github.com/nccgroup/ScoutSuite/blob/master/ScoutSuite/providers/aws/resources/awslambda/service.py). When calling `fetch_all` on the children, `Regions` will pass a region in the scope.

You will need to pass the facade and the service name in the super constructor. The service name is used by `Regions` to build a list of all the regions. 

## Vpcs

`Vpcs` works a bit like regions, but on another level. It will fetch children in the VPCs located in a given region. When calling `fetch_all` on the children, it will pass a region and a VPC id in the scope.

# Azure

Azure support only defines `AzureResources` that inherits from the base class `Resources` and `AzureCompositeResources` that inherits from `CompositeResources`. Although, those classes are currently empty (their implementation is just `pass`), they are used in the case where some Azure-specific processing could be defined and added to those classes.
Currently, there's no hierarchy like AWS `Regions`, `VPCs` or GCP `Projects`, `Regions` and `Zones`.

# GCP

GCP has three implementations of `CompositeResources` you may use to simplify the implementation of new services: `Projects`, `Regions` and `Zones`.

## Projects

In Google Cloud Platform, resources must be part of a project. Our architecture reflects this by having the base class of GCP services inherit from the `Projects` class. This class itself inherits from `CompositeResources` and therefore behaves in the same way, with the addition of fetching the GCP projects and grouping it's children resources per project.

## Regions

In Google Cloud Platform, additionally to having to be part of a project, certain resources must also have a given region. An example of such resources, are Subnets (or Subnetworks). This is reflected in our architecture with the `Regions` and `GCERegions` classes. The `Regions` class is similar to the `Projects` class, it inherits from `CompositeResources` and takes care of fetching the regions before grouping its children resource by region. The `GCERegions` class is an implementation of the `Regions` class that acts as the parent of Google Compute Engine resources that have a region (ie. `Subnetworks`).

## Zones

In Google Cloud Platform, additionally to having to be part of a project, certain resources must also have a given zone. An example of such resources, are Google Compute Engine Instances and Google Kubernetes Engine Clusters. This is reflected in our architecture with the `Zones`, `GCEZones` and `GKEZones` classes. The `Zones` class is similar to the `Projects` class, it inherits from `CompositeResources` and takes care of fetching the zones before grouping its children resource by zone. The `GCEZones` and `GKEZones` classes are implementations of the `Zones` class for GCE and GKE respectively. They act as the parent of resources that have a zone (ie. `Instances` and `Clusters`).