# {{ projectName|replace("_", " ") }} Strings SDK
This project and this README has been generated using [Localiser](https://github.com/gotev/localiser).

All the files contained in this directory and its subdirectories are subject to the attached [license](LICENSE).

## What's inside
An android library module, ready to be deployed, which has:

* A values `xml` file for each one of the namespaces in each one of the supported languages
* `{{ projectShortIdentifier|capitalize }}Strings` class which contains kotlin type-safe mappings for each localised string

## How to use it
Add this to your gradle: 

```groovy
implementation '{{ projectGroup }}:{{ moduleName }}:{{ projectVersion }}'
```

If you are using your own repository, add also:

```groovy
maven { url "https://path/to/your/repository" }
```
in the repositories section of your gradle.

Sync the project and inject application context:

```kotlin
class App : Application() {
    override fun onCreate() {
        super.onCreate()
        
        {{ projectShortIdentifier|capitalize }}Strings.context = this
    }
}
```

Then get strings like this

```kotlin
val value = String.{{ projectShortIdentifier }}.namespace.yourLocalisationKey()
```

If a string has placeholders, the generated functions will have also parameters. Each parameter type is `String`.

### Example
Let's say we have a namespace called `homepage` in which we have two localisation keys:

* `<string name="title">Home Page</string>`
* `<string name="greeting">Hello ${name}, your customer code is ${customerCode}</string>`

This is how to use them in the code:

```kotlin
val title = String.{{ projectShortIdentifier }}.homepage.title()
val greeting = String.{{ projectShortIdentifier }}.homepage.greeting(name = "Alfred", customerCode = "A5GH99")
```

## Generate framework
### Prerequisites
* [Java 8+](https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)
* [Android Studio](https://developer.android.com/studio)
* Have `ANDROID_SDK_ROOT` in your environment variables.
  * On macOS add `export ANDROID_SDK_ROOT=/path/to/android/sdk` to your `~/.zshrc` and then `source ~/.zshrc`

### Generation
It's recommended to deploy this strings SDK to either:
* Local maven repository, for local development
* Your Nexus (or Artifactory) server, for internal usage in an organization

#### Local Maven repository
{% if projectInternalMavenRepo is none %}* Setup the environment variable `LOCAL_MAVEN_URL` to point to your local maven repository{% endif %}

Execute: 
```
./gradlew clean build publish -PmavPublishToInternalRepo=true
```

#### Nexus (or Artifactory)
{% if projectNexusMavenRepo is none %}* Setup the environment variable `NEXUS_MAVEN_URL` to point to your maven repository{% endif %}

* Add `NEXUS_USER` and `NEXUS_PASSWORD` to your environment variables (never store passwords in a repo)

Execute:
```
./gradlew clean build publish -PmavPublishToRemoteRepo=true -PmavRemoteRepoUser=$NEXUS_USER -PmavRemoteRepoPassword=$NEXUS_PASSWORD
```
