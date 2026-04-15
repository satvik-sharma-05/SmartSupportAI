import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import {
    BarChart3,
    TrendingUp,
    AlertCircle,
    Clock,
    Activity,
    Users,
    Zap
} from 'lucide-react'
import { PieChart, Pie, Cell, BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import DashboardLayout from '../layouts/DashboardLayout'
import { apiService } from '../services/api'
import toast from 'react-hot-toast'

const Dashboard = () => {
    const [stats, setStats] = useState(null)
    const [tickets, setTickets] = useState([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetchData()
    }, [])

    const fetchData = async () => {
        try {
            setLoading(true)
            const [statsData, ticketsData] = await Promise.all([
                apiService.getStatistics(),
                apiService.getTickets(10)
            ])
            setStats(statsData)
            setTickets(ticketsData.tickets || [])
        } catch (error) {
            toast.error('Failed to load dashboard data')
            console.error(error)
        } finally {
            setLoading(false)
        }
    }

    // Mock data for demo
    const mockStats = {
        total_tickets: 1523,
        total_predictions: 1523,
        category_distribution: [
            { _id: 'Technical', count: 612 },
            { _id: 'Billing', count: 445 },
            { _id: 'Account', count: 289 },
            { _id: 'General', count: 177 }
        ],
        priority_distribution: [
            { _id: 'High', count: 523 },
            { _id: 'Medium', count: 678 },
            { _id: 'Low', count: 322 }
        ],
        avg_inference_time_ms: [{ _id: null, avg_time: 142.56 }]
    }

    const displayStats = stats || mockStats

    const statCards = [
        {
            title: 'Total Tickets',
            value: displayStats.total_tickets?.toLocaleString() || '0',
            icon: <Activity className="w-6 h-6" />,
            color: 'from-blue-500 to-blue-600',
            change: '+12.5%',
            changeType: 'increase'
        },
        {
            title: 'High Priority',
            value: displayStats.priority_distribution?.find(p => p._id === 'High')?.count || 0,
            icon: <AlertCircle className="w-6 h-6" />,
            color: 'from-red-500 to-red-600',
            change: '+8.2%',
            changeType: 'increase'
        },
        {
            title: 'Categories',
            value: displayStats.category_distribution?.length || 4,
            icon: <BarChart3 className="w-6 h-6" />,
            color: 'from-green-500 to-green-600',
            change: 'Stable',
            changeType: 'neutral'
        },
        {
            title: 'Avg Response',
            value: `${displayStats.avg_inference_time_ms?.[0]?.avg_time?.toFixed(0) || 142}ms`,
            icon: <Zap className="w-6 h-6" />,
            color: 'from-purple-500 to-purple-600',
            change: '-5.3%',
            changeType: 'decrease'
        }
    ]

    // Chart data
    const categoryData = displayStats.category_distribution?.map(item => ({
        name: item._id,
        value: item.count
    })) || []

    const priorityData = displayStats.priority_distribution?.map(item => ({
        name: item._id,
        value: item.count
    })) || []

    const trendData = [
        { name: 'Mon', tickets: 245 },
        { name: 'Tue', tickets: 312 },
        { name: 'Wed', tickets: 289 },
        { name: 'Thu', tickets: 356 },
        { name: 'Fri', tickets: 421 },
        { name: 'Sat', tickets: 198 },
        { name: 'Sun', tickets: 167 }
    ]

    const COLORS = {
        Technical: '#3b82f6',
        Billing: '#10b981',
        Account: '#f59e0b',
        General: '#8b5cf6',
        High: '#ef4444',
        Medium: '#f59e0b',
        Low: '#10b981'
    }

    if (loading) {
        return (
            <DashboardLayout>
                <div className="flex items-center justify-center h-96">
                    <div className="text-center">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                        <p className="text-gray-600">Loading dashboard...</p>
                    </div>
                </div>
            </DashboardLayout>
        )
    }

    return (
        <DashboardLayout>
            <div className="space-y-6">
                {/* Header */}
                <div>
                    <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
                    <p className="text-gray-600 mt-1">Welcome back! Here's what's happening today.</p>
                </div>

                {/* Stats Cards */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {statCards.map((stat, index) => (
                        <motion.div
                            key={index}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.3, delay: index * 0.1 }}
                            className="card"
                        >
                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="text-sm text-gray-600 mb-1">{stat.title}</p>
                                    <p className="text-3xl font-bold text-gray-900">{stat.value}</p>
                                    <p className={`text-sm mt-2 ${stat.changeType === 'increase' ? 'text-green-600' :
                                            stat.changeType === 'decrease' ? 'text-red-600' :
                                                'text-gray-600'
                                        }`}>
                                        {stat.change} from last week
                                    </p>
                                </div>
                                <div className={`w-14 h-14 bg-gradient-to-br ${stat.color} rounded-xl flex items-center justify-center text-white`}>
                                    {stat.icon}
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </div>

                {/* Charts Row */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* Category Distribution */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3, delay: 0.4 }}
                        className="card"
                    >
                        <h3 className="text-lg font-semibold mb-4">Category Distribution</h3>
                        <ResponsiveContainer width="100%" height={300}>
                            <PieChart>
                                <Pie
                                    data={categoryData}
                                    cx="50%"
                                    cy="50%"
                                    labelLine={false}
                                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                                    outerRadius={100}
                                    fill="#8884d8"
                                    dataKey="value"
                                >
                                    {categoryData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[entry.name]} />
                                    ))}
                                </Pie>
                                <Tooltip />
                            </PieChart>
                        </ResponsiveContainer>
                    </motion.div>

                    {/* Priority Distribution */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3, delay: 0.5 }}
                        className="card"
                    >
                        <h3 className="text-lg font-semibold mb-4">Priority Distribution</h3>
                        <ResponsiveContainer width="100%" height={300}>
                            <BarChart data={priorityData}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                                <XAxis dataKey="name" />
                                <YAxis />
                                <Tooltip />
                                <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                                    {priorityData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[entry.name]} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </motion.div>
                </div>

                {/* Ticket Trends */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3, delay: 0.6 }}
                    className="card"
                >
                    <h3 className="text-lg font-semibold mb-4">Ticket Trends (Last 7 Days)</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <LineChart data={trendData}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                            <XAxis dataKey="name" />
                            <YAxis />
                            <Tooltip />
                            <Line
                                type="monotone"
                                dataKey="tickets"
                                stroke="#3b82f6"
                                strokeWidth={3}
                                dot={{ fill: '#3b82f6', r: 6 }}
                                activeDot={{ r: 8 }}
                            />
                        </LineChart>
                    </ResponsiveContainer>
                </motion.div>

                {/* Recent Tickets Table */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3, delay: 0.7 }}
                    className="card"
                >
                    <h3 className="text-lg font-semibold mb-4">Recent Tickets</h3>
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead>
                                <tr className="border-b border-gray-200">
                                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Ticket</th>
                                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Category</th>
                                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Priority</th>
                                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Time</th>
                                </tr>
                            </thead>
                            <tbody>
                                {tickets.length > 0 ? (
                                    tickets.slice(0, 5).map((ticket, index) => (
                                        <tr key={index} className="border-b border-gray-100 hover:bg-gray-50 transition-colors">
                                            <td className="py-3 px-4 text-sm text-gray-900 max-w-md truncate">
                                                {ticket.text}
                                            </td>
                                            <td className="py-3 px-4">
                                                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                                    {ticket.category || 'N/A'}
                                                </span>
                                            </td>
                                            <td className="py-3 px-4">
                                                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${ticket.priority === 'High' ? 'bg-red-100 text-red-800' :
                                                        ticket.priority === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                                                            'bg-green-100 text-green-800'
                                                    }`}>
                                                    {ticket.priority || 'N/A'}
                                                </span>
                                            </td>
                                            <td className="py-3 px-4 text-sm text-gray-600">
                                                {ticket.created_at ? new Date(ticket.created_at).toLocaleString() : 'N/A'}
                                            </td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan="4" className="py-8 text-center text-gray-500">
                                            No tickets yet. Start by making predictions!
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </motion.div>
            </div>
        </DashboardLayout>
    )
}

export default Dashboard
