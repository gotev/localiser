package com.my.org

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

val String.Companion.myapp: MyappStrings
    get() = MyappStrings

@SuppressLint("StaticFieldLeak")
object MyappStrings {
    lateinit var context: Context
    val feature_2 by lazy { MyappFeature_2Strings(context) }
    val feature1 by lazy { MyappFeature1Strings(context) }
}