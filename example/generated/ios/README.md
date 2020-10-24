# TestApp Strings SDK
This project and this README has been generated using [Localiser](https://github.com/gotev/localiser). 

All the files contained in this directory and its subdirectories are subject to the attached [license](LICENSE).

## What's inside
* A `.lproj` directory for each one of the supported languages
* A `LocaliserExtensions` directory which contains swift type-safe mappings for each localised string

## How to use it
* Import this repo in your project as a Swift Package Manager
* Add `import TestAppStrings` to your swift source files where you want to use localised strings 

and then use it like this:

```swift
let value = String.myapp.namespace.yourLocalisationKey()
```

If a string has placeholders, the generated functions will have also parameters. Each parameter type is `CustomStringConvertible`.

### Example
Let's say we have a namespace called `homepage` in which we have two localisation keys:

* `"title" = "Home Page";`
* `"greeting" = "Hello ${name}, your customer code is ${customerCode}";`

This is how to use them in the code:

```swift
let title = String.myapp.homepage.title()
let greeting = String.myapp.homepage.greeting(name: "Alfred", customerCode: "A5GH99")
```