# Localiser Vision

The reason this has been developed is because as a mobile developer working on both iOS and Android native applications, there is a need to be able to manage localisation strings in a single place, avoid common mistakes, be fast and reliable. Most of all, have something which is totally free and community driven, to be able to evolve it and make it always support the latest Android and iOS additions.

## Goals
* Have simple serverless Web UI to manage localisation strings for multiple projects. SQLite has been chosen to be able to have a single portable file which contains all it's needed, and from which data can be exported in a variety of ways.
* For each project, be able to group strings. These are called namespaces. You can call them features, sections or whatever suits best your specific case. A general naming has been used on purpose.
* Be able to manage many different languages for each project, keeping them consistent and avoiding common errors
* Have an auto generated iOS framework and Android library to add to your native iOS/Android app, which contains all the localized resources needed.
* Be compliant with Apple and Google best practices about localization
* Support all the features you will normally have in Xcode and Android Studio
* Use strings in a type-safe way inside the project, calling swift and kotlin functions
* Support named placeholders
* Use code-generation as much as it's needed to have native libraries without third party dependencies and which can be easily read and modified by anyone in your team if needed.
* Be Continuous-Integration friendly and ease all DevOps operations
* Be fast when new localisation strings are added or modified and have rapid feedback in your app, directly from Xcode and Android Studio
* Have an easily maintainable codebase which is easy to evolve and not too vast. It's better to give up on customization and use as much as the defaults allows, be it for Jinja2, for Django or for Python itself. Going in deeper customization leads to more difficulties making the project go forward and finding developers who wants to contribute. Of course, there may be exceptions to this goal.
* Extend export to other formats other than Android and iOS

The future is bright and many things can change over the course of time, but this document will always reflect the direction of this project.
