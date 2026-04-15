import React, { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
    LayoutDashboard,
    Sparkles,
    Target,
    LogOut,
    Menu,
    X,
    User,
    Settings,
    Bell
} from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import toast from 'react-hot-toast'

const DashboardLayout = ({ children }) => {
    const [sidebarOpen, setSidebarOpen] = useState(false)
    const [userMenuOpen, setUserMenuOpen] = useState(false)
    const { user, logout } = useAuth()
    const location = useLocation()
    const navigate = useNavigate()

    const navigation = [
        { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
        { name: 'Predict', href: '/predict', icon: Target },
    ]

    const handleLogout = () => {
        logout()
        toast.success('Logged out successfully')
        navigate('/login')
    }

    const isActive = (path) => location.pathname === path

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
            {/* Sidebar - Desktop */}
            <aside className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-64 lg:flex-col">
                <div className="flex flex-col flex-grow glass border-r border-white/20 pt-5 pb-4 overflow-y-auto">
                    {/* Logo */}
                    <div className="flex items-center flex-shrink-0 px-4 mb-8">
                        <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center">
                            <Sparkles className="w-6 h-6 text-white" />
                        </div>
                        <span className="ml-3 text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                            SmartSupport AI
                        </span>
                    </div>

                    {/* Navigation */}
                    <nav className="flex-1 px-3 space-y-2">
                        {navigation.map((item) => {
                            const Icon = item.icon
                            const active = isActive(item.href)
                            return (
                                <Link
                                    key={item.name}
                                    to={item.href}
                                    className={`group flex items-center px-3 py-3 text-sm font-medium rounded-lg transition-all duration-200 ${active
                                            ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg'
                                            : 'text-gray-700 hover:bg-white/50'
                                        }`}
                                >
                                    <Icon className={`mr-3 h-5 w-5 ${active ? 'text-white' : 'text-gray-500 group-hover:text-blue-600'}`} />
                                    {item.name}
                                </Link>
                            )
                        })}
                    </nav>

                    {/* User Section */}
                    <div className="flex-shrink-0 px-3 pb-4">
                        <div className="glass rounded-lg p-3">
                            <div className="flex items-center">
                                <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-500 rounded-full flex items-center justify-center text-white font-semibold">
                                    {user?.name?.charAt(0).toUpperCase() || 'U'}
                                </div>
                                <div className="ml-3 flex-1">
                                    <p className="text-sm font-medium text-gray-900">{user?.name || 'User'}</p>
                                    <p className="text-xs text-gray-500 truncate">{user?.email || 'user@example.com'}</p>
                                </div>
                            </div>
                            <button
                                onClick={handleLogout}
                                className="mt-3 w-full flex items-center justify-center px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                            >
                                <LogOut className="w-4 h-4 mr-2" />
                                Logout
                            </button>
                        </div>
                    </div>
                </div>
            </aside>

            {/* Mobile sidebar */}
            {sidebarOpen && (
                <div className="lg:hidden">
                    <div className="fixed inset-0 z-40 flex">
                        <div
                            className="fixed inset-0 bg-gray-600 bg-opacity-75"
                            onClick={() => setSidebarOpen(false)}
                        ></div>
                        <motion.div
                            initial={{ x: -300 }}
                            animate={{ x: 0 }}
                            exit={{ x: -300 }}
                            className="relative flex-1 flex flex-col max-w-xs w-full glass"
                        >
                            <div className="absolute top-0 right-0 -mr-12 pt-2">
                                <button
                                    onClick={() => setSidebarOpen(false)}
                                    className="ml-1 flex items-center justify-center h-10 w-10 rounded-full focus:outline-none"
                                >
                                    <X className="h-6 w-6 text-white" />
                                </button>
                            </div>
                            <div className="flex-1 h-0 pt-5 pb-4 overflow-y-auto">
                                <div className="flex items-center flex-shrink-0 px-4 mb-8">
                                    <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center">
                                        <Sparkles className="w-6 h-6 text-white" />
                                    </div>
                                    <span className="ml-3 text-xl font-bold">SmartSupport AI</span>
                                </div>
                                <nav className="px-3 space-y-2">
                                    {navigation.map((item) => {
                                        const Icon = item.icon
                                        const active = isActive(item.href)
                                        return (
                                            <Link
                                                key={item.name}
                                                to={item.href}
                                                onClick={() => setSidebarOpen(false)}
                                                className={`group flex items-center px-3 py-3 text-sm font-medium rounded-lg ${active
                                                        ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white'
                                                        : 'text-gray-700 hover:bg-white/50'
                                                    }`}
                                            >
                                                <Icon className="mr-3 h-5 w-5" />
                                                {item.name}
                                            </Link>
                                        )
                                    })}
                                </nav>
                            </div>
                        </motion.div>
                    </div>
                </div>
            )}

            {/* Main content */}
            <div className="lg:pl-64 flex flex-col flex-1">
                {/* Top bar */}
                <div className="glass sticky top-0 z-10 flex-shrink-0 flex h-16 border-b border-white/20">
                    <button
                        onClick={() => setSidebarOpen(true)}
                        className="px-4 text-gray-500 focus:outline-none lg:hidden"
                    >
                        <Menu className="h-6 w-6" />
                    </button>
                    <div className="flex-1 px-4 flex justify-between items-center">
                        <div className="flex-1"></div>
                        <div className="ml-4 flex items-center space-x-4">
                            <button className="p-2 text-gray-500 hover:text-gray-700 rounded-lg hover:bg-white/50 transition-colors">
                                <Bell className="h-5 w-5" />
                            </button>
                            <button className="p-2 text-gray-500 hover:text-gray-700 rounded-lg hover:bg-white/50 transition-colors">
                                <Settings className="h-5 w-5" />
                            </button>
                        </div>
                    </div>
                </div>

                {/* Page content */}
                <main className="flex-1">
                    <div className="py-6 px-4 sm:px-6 lg:px-8">
                        {children}
                    </div>
                </main>
            </div>
        </div>
    )
}

export default DashboardLayout
