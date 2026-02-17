package com.bme688.sensorapp

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity

/**
 * MainActivity - شاشة البداية الرئيسية
 * توفر الوصول إلى جميع أوضاع التشغيل
 */
class MainMenuActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main_menu)
        supportActionBar?.title = "X-Bio • القائمة الرئيسية"

        setupMenuButtons()
    }

    private fun setupMenuButtons() {
        // زر المراقبة المباشرة
        findViewById<Button>(R.id.btnMonitor)?.setOnClickListener {
            startActivity(Intent(this, MainActivity::class.java))
        }

        // زر تدريب الرائحة
        findViewById<Button>(R.id.btnTraining)?.setOnClickListener {
            startActivity(Intent(this, TrainingActivity::class.java))
        }

        // زر الاستكشاف
        findViewById<Button>(R.id.btnDetection)?.setOnClickListener {
            startActivity(Intent(this, DetectionActivity::class.java))
        }

        // زر الإحصائيات
        findViewById<Button>(R.id.btnStatistics)?.setOnClickListener {
            startActivity(Intent(this, StatisticsActivity::class.java))
        }
    }
}
