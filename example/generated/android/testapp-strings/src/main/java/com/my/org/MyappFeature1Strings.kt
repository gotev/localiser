package com.my.org

import android.content.Context
import com.my.org.R

class MyappFeature1Strings(private val context: Context) {

    // This is a test comment meant to check if everything is ok
    fun test1(name: String) =
        context.getString(R.string.feature1_test1)
            .replace("\${name}", name)

    fun test2() =
        context.getString(R.string.feature1_test2)

    // This is a test comment meant to check if everything is ok on
    // test3
    fun test3() =
        context.getString(R.string.feature1_test3)
}