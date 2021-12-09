# Table of contents
* [Introduction](#introduction)
* [Core](#core)
* [Output](#output)
* [Providers](#providers)

# Introduction

The objective of this page is to give a high-level overview of Scout Suite's architecture. Below is a simplified package diagram you can use to follow along. 

![](https://i.imgur.com/HaNlbBE.jpg)

# Core
The __core__ module contains the rule processing engine, the command line interface logic, logging methods and some utils.

# Output
The __output__ module contains the logic used to transform the scanned data into a web report. The web report scaffolding is located inside the __output.data.inc-scoutsuite__ submodule.

# Providers
The __providers__ module contains all the data fetching logic. You can learn more about it in this [article](https://github.com/nccgroup/ScoutSuite/wiki/Resources-fetching-system-architecture).