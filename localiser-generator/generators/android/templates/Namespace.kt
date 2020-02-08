package {{ projectPackage }}

import android.content.Context
import {{ projectPackage }}.R

class {{ projectShortIdentifier|capitalize }}{{ projectNamespace|capitalize }}Strings(private val context: Context) {
{% for translationFunction in translationFunctions %}

    {% if translationFunction['localisedKeyComment'] is not none %}
    {% for commentLine in translationFunction['localisedKeyComment'] %}
    {{ commentLine }}
    {% endfor %}
    {% endif %}
    fun {{ translationFunction['name'] }}({{ translationFunction['parameters'] }}) =
        context.getString(R.string.{{ translationFunction['localisedKey'] }})
            {% for placeholder in translationFunction['placeholders'] %}
            .replace("{{ placeholder['placeholder'] }}", {{ placeholder['variableName'] }})
            {% endfor %}
            {% if translationFunction['localisedKeyValueContainsHTML'] %}
            .fromHTML()
            {% endif %}
{% endfor %}
}