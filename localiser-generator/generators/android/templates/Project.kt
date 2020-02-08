package {{ projectPackage }}

import android.annotation.SuppressLint
import android.content.Context
import android.os.Build
import android.text.Html

@Suppress("DEPRECATION")
fun String.fromHTML() = if (Build.VERSION.SDK_INT >= 24) {
        Html.fromHtml(this, Html.FROM_HTML_MODE_LEGACY)
    } else {
        Html.fromHtml(this)
    }

val String.Companion.{{ projectShortIdentifier }}: {{ projectShortIdentifier|capitalize }}Strings
    get() = {{ projectShortIdentifier|capitalize }}Strings

@SuppressLint("StaticFieldLeak")
object {{ projectShortIdentifier|capitalize }}Strings {
    lateinit var context: Context
{% for projectNamespace in projectNamespaces %}
    val {{ projectNamespace }} by lazy { {{ projectShortIdentifier|capitalize }}{{ projectNamespace|capitalize }}Strings(context) }
{% endfor %}
}
