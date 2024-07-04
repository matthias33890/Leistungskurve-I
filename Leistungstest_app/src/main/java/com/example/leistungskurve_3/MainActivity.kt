package com.example.leistungskurve_3

import android.os.Bundle
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.viewinterop.AndroidView
import androidx.compose.ui.tooling.preview.Preview
import com.example.leistungskurve_3.ui.theme.Leistungskurve_3Theme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            Leistungskurve_3Theme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    WebViewScreen(
                        url = "https://uni.ravexserver.duckdns.org/",
                        modifier = Modifier.padding(innerPadding)
                    )
                }
            }
        }
    }
}

@Composable
fun WebViewScreen(url: String, modifier: Modifier = Modifier) {
    AndroidView(factory = { context ->
        WebView(context).apply {
            webViewClient = WebViewClient()
            settings.javaScriptEnabled = true // Falls deine Website JavaScript benötigt
            loadUrl(url)
        }
    }, modifier = modifier.fillMaxSize())
}

@Preview(showBackground = true)
@Composable
fun WebViewScreenPreview() {
    Leistungskurve_3Theme {
        WebViewScreen("https://uni.ravexserver.duckdns.org/")
    }
}
