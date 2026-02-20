import React, { useState, useEffect } from 'react';
import { Card } from '@/Components/ui/card';
import { 
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  AreaChart, Area, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis
} from 'recharts';
import { supabase } from '@/api/supabaseClient';

const AnalyticsDashboardPage = () => {
  const [analytics, setAnalytics] = useState({
    overview: {
      totalManuscripts: 0,
      totalWords: 0,
      totalReads: 0,
      avgRating: 0,
      growthRate: 0
    },
    manuscriptStats: [],
    genreDistribution: [],
    readingTrends: [],
    userEngagement: [],
    performanceMetrics: []
  });

  const [timeRange, setTimeRange] = useState('7d'); // 7d, 30d, 90d, 1y
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAnalytics();
  }, [timeRange]);

  const loadAnalytics = async () => {
    setLoading(true);
    try {
      // في بيئة production، هذه البيانات ستأتي من Supabase
      // هنا نستخدم بيانات تجريبية للعرض
      
      const mockData = {
        overview: {
          totalManuscripts: 24,
          totalWords: 245890,
          totalReads: 12450,
          avgRating: 4.5,
          growthRate: 23.5
        },
        manuscriptStats: [
          { name: 'رواية الحب الأول', words: 52000, reads: 3200, rating: 4.7, status: 'منشورة' },
          { name: 'قصة المغامرة', words: 18500, reads: 1800, rating: 4.5, status: 'منشورة' },
          { name: 'ديوان الشعر', words: 8200, reads: 950, rating: 4.3, status: 'منشورة' },
          { name: 'رواية الغموض', words: 45000, reads: 2100, rating: 4.6, status: 'قيد المراجعة' },
          { name: 'مقالات فلسفية', words: 12500, reads: 680, rating: 4.1, status: 'مسودة' }
        ],
        genreDistribution: [
          { name: 'رواية', value: 10, color: '#3b82f6' },
          { name: 'قصة قصيرة', value: 6, color: '#10b981' },
          { name: 'شعر', value: 4, color: '#f59e0b' },
          { name: 'مقال', value: 3, color: '#ef4444' },
          { name: 'دراسة', value: 1, color: '#8b5cf6' }
        ],
        readingTrends: [
          { date: '1 يناير', reads: 450, likes: 120, shares: 30 },
          { date: '5 يناير', reads: 680, likes: 180, shares: 45 },
          { date: '10 يناير', reads: 920, likes: 250, shares: 60 },
          { date: '15 يناير', reads: 1200, likes: 340, shares: 85 },
          { date: '20 يناير', reads: 1450, likes: 420, shares: 105 }
        ],
        userEngagement: [
          { metric: 'القراءة', value: 85 },
          { metric: 'الإعجاب', value: 65 },
          { metric: 'المشاركة', value: 45 },
          { metric: 'التعليق', value: 35 },
          { metric: 'الحفظ', value: 55 },
          { metric: 'المتابعة', value: 70 }
        ],
        performanceMetrics: [
          { month: 'يناير', manuscripts: 24, reads: 12450, engagement: 68 },
          { month: 'ديسمبر', manuscripts: 22, reads: 10800, engagement: 62 },
          { month: 'نوفمبر', manuscripts: 20, reads: 9200, engagement: 58 },
          { month: 'أكتوبر', manuscripts: 18, reads: 7600, engagement: 54 },
          { month: 'سبتمبر', manuscripts: 16, reads: 6300, engagement: 50 },
          { month: 'أغسطس', manuscripts: 14, reads: 5100, engagement: 46 }
        ]
      };

      setAnalytics(mockData);
    } catch (error) {
      console.error('Error loading analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  const StatCard = ({ title, value, subtitle, icon, trend }) => (
    <Card className="p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-start justify-between">
        <div className="space-y-2">
          <p className="text-sm text-gray-600">{title}</p>
          <p className="text-3xl font-bold text-gray-900">{value}</p>
          {subtitle && <p className="text-sm text-gray-500">{subtitle}</p>}
        </div>
        <div className="text-4xl">{icon}</div>
      </div>
      {trend && (
        <div className={`mt-4 text-sm font-medium ${trend > 0 ? 'text-green-600' : 'text-red-600'}`}>
          {trend > 0 ? '↑' : '↓'} {Math.abs(trend)}% من الشهر الماضي
        </div>
      )}
    </Card>
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">جاري تحميل التحليلات...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-8" dir="rtl">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">📊 لوحة التحليلات</h1>
        <p className="text-gray-600">تحليل شامل لأداء مخطوطاتك وتفاعل القراء</p>
      </div>

      {/* Time Range Selector */}
      <div className="mb-6 flex gap-2">
        {[
          { label: '7 أيام', value: '7d' },
          { label: '30 يوم', value: '30d' },
          { label: '90 يوم', value: '90d' },
          { label: 'سنة', value: '1y' }
        ].map(range => (
          <button
            key={range.value}
            onClick={() => setTimeRange(range.value)}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              timeRange === range.value
                ? 'bg-blue-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-100'
            }`}
          >
            {range.label}
          </button>
        ))}
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="إجمالي المخطوطات"
          value={analytics.overview.totalManuscripts}
          icon="📚"
          trend={15}
        />
        <StatCard
          title="إجمالي الكلمات"
          value={analytics.overview.totalWords.toLocaleString()}
          icon="📝"
          trend={23.5}
        />
        <StatCard
          title="إجمالي القراءات"
          value={analytics.overview.totalReads.toLocaleString()}
          icon="👁️"
          trend={18}
        />
        <StatCard
          title="متوسط التقييم"
          value={analytics.overview.avgRating.toFixed(1)}
          subtitle="من 5.0"
          icon="⭐"
          trend={5}
        />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Reading Trends */}
        <Card className="p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">📈 اتجاهات القراءة</h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={analytics.readingTrends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Area type="monotone" dataKey="reads" stackId="1" stroke="#3b82f6" fill="#3b82f6" name="القراءات" />
              <Area type="monotone" dataKey="likes" stackId="1" stroke="#10b981" fill="#10b981" name="الإعجابات" />
              <Area type="monotone" dataKey="shares" stackId="1" stroke="#f59e0b" fill="#f59e0b" name="المشاركات" />
            </AreaChart>
          </ResponsiveContainer>
        </Card>

        {/* Genre Distribution */}
        <Card className="p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">🎯 توزيع الأنواع الأدبية</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={analytics.genreDistribution}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {analytics.genreDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </Card>

        {/* Manuscript Performance */}
        <Card className="p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">📊 أداء المخطوطات</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={analytics.manuscriptStats}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="reads" fill="#3b82f6" name="القراءات" />
              <Bar dataKey="rating" fill="#10b981" name="التقييم (×1000)" />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        {/* User Engagement Radar */}
        <Card className="p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">💫 تفاعل المستخدمين</h3>
          <ResponsiveContainer width="100%" height={300}>
            <RadarChart data={analytics.userEngagement}>
              <PolarGrid />
              <PolarAngleAxis dataKey="metric" />
              <PolarRadiusAxis angle={90} domain={[0, 100]} />
              <Radar name="التفاعل" dataKey="value" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.6} />
              <Tooltip />
            </RadarChart>
          </ResponsiveContainer>
        </Card>
      </div>

      {/* Performance Timeline */}
      <Card className="p-6 mb-8">
        <h3 className="text-xl font-bold text-gray-900 mb-4">📅 الأداء عبر الزمن</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={analytics.performanceMetrics}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis yAxisId="left" />
            <YAxis yAxisId="right" orientation="left" />
            <Tooltip />
            <Legend />
            <Line yAxisId="left" type="monotone" dataKey="manuscripts" stroke="#3b82f6" name="المخطوطات" strokeWidth={2} />
            <Line yAxisId="left" type="monotone" dataKey="reads" stroke="#10b981" name="القراءات (÷100)" strokeWidth={2} />
            <Line yAxisId="right" type="monotone" dataKey="engagement" stroke="#f59e0b" name="التفاعل %" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </Card>

      {/* Top Manuscripts Table */}
      <Card className="p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">🏆 أفضل المخطوطات أداءً</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-right">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-sm font-medium text-gray-700">#</th>
                <th className="px-4 py-3 text-sm font-medium text-gray-700">العنوان</th>
                <th className="px-4 py-3 text-sm font-medium text-gray-700">الكلمات</th>
                <th className="px-4 py-3 text-sm font-medium text-gray-700">القراءات</th>
                <th className="px-4 py-3 text-sm font-medium text-gray-700">التقييم</th>
                <th className="px-4 py-3 text-sm font-medium text-gray-700">الحالة</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {analytics.manuscriptStats.map((manuscript, index) => (
                <tr key={index} className="hover:bg-gray-50">
                  <td className="px-4 py-3 text-sm">{index + 1}</td>
                  <td className="px-4 py-3 text-sm font-medium">{manuscript.name}</td>
                  <td className="px-4 py-3 text-sm">{manuscript.words.toLocaleString()}</td>
                  <td className="px-4 py-3 text-sm">{manuscript.reads.toLocaleString()}</td>
                  <td className="px-4 py-3 text-sm">
                    <div className="flex items-center gap-1">
                      <span className="text-yellow-500">⭐</span>
                      <span>{manuscript.rating}</span>
                    </div>
                  </td>
                  <td className="px-4 py-3 text-sm">
                    <span className={`px-2 py-1 rounded-full text-xs ${
                      manuscript.status === 'منشورة' 
                        ? 'bg-green-100 text-green-800'
                        : manuscript.status === 'قيد المراجعة'
                        ? 'bg-blue-100 text-blue-800'
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {manuscript.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Export Analytics Button */}
      <div className="mt-8 flex justify-center">
        <button className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-medium hover:shadow-lg transition-shadow">
          📥 تصدير التحليلات (PDF)
        </button>
      </div>
    </div>
  );
};

export default AnalyticsDashboardPage;
