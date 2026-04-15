import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Send, RotateCcw, Sparkles, TrendingUp, Target, Clock } from 'lucide-react'
import DashboardLayout from '../layouts/DashboardLayout'
import { apiService } from '../services/api'
import toast from 'react-hot-toast'

const PredictPage = () => {
    const [ticketText, setTicketText] = useState('')
    const [prediction, setPrediction] = useState(null)
    const [loading, setLoading] = useState(false)

    const exampleTickets = [
        "I was charged twice for my subscription this month",
        "Cannot login to my account, getting error 500",
        "How do I change my password?",
        "What features are included in the pro plan?"
    ]

    const handlePredict = async () => {
        if (!ticketText.trim()) {
            toast.error('Please enter a ticket description')
            return
        }

        if (ticketText.length < 10) {
            toast.error('Ticket text must be at least 10 characters')
            return
        }

        setLoading(true)
        setPrediction(null)

        try {
            const result = await apiService.predictTicket(ticketText)
            setPrediction(result)
            toast.success('Ticket classified successfully!')
        } catch (error) {
            toast.error(error.response?.data?.detail || 'Prediction failed. Please try again.')
            console.error(error)
        } finally {
            setLoading(false)
        }
    }

    const handleReset = () => {
        setTicketText('')
        setPrediction(null)
    }

    const handleExampleClick = (example) => {
        setTicketText(example)
        setPrediction(null)
    }

    const getCategoryColor = (category) => {
        const colors = {
            'Billing': 'from-green-500 to-green-600',
            'Technical': 'from-blue-500 to-blue-600',
            'Account': 'from-yellow-500 to-yellow-600',
            'General': 'from-purple-500 to-purple-600'
        }
        return colors[category] || 'from-gray-500 to-gray-600'
    }

    const getPriorityColor = (priority) => {
        const colors = {
            'High': 'from-red-500 to-red-600',
            'Medium': 'from-yellow-500 to-yellow-600',
            'Low': 'from-green-500 to-green-600'
        }
        return colors[priority] || 'from-gray-500 to-gray-600'
    }

    return (
        <DashboardLayout>
            <div className="max-w-5xl mx-auto space-y-6">
                {/* Header */}
                <div>
                    <h1 className="text-3xl font-bold text-gray-900">Ticket Prediction</h1>
                    <p className="text-gray-600 mt-1">
                        Use AI to automatically classify and prioritize support tickets
                    </p>
                </div>

                {/* Main Card */}
                <div className="grid lg:grid-cols-2 gap-6">
                    {/* Input Section */}
                    <motion.div
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.3 }}
                        className="card"
                    >
                        <div className="flex items-center space-x-2 mb-4">
                            <Sparkles className="w-5 h-5 text-blue-600" />
                            <h2 className="text-xl font-semibold">Enter Ticket</h2>
                        </div>

                        <textarea
                            value={ticketText}
                            onChange={(e) => setTicketText(e.target.value)}
                            placeholder="Describe the support ticket here... (minimum 10 characters)"
                            className="w-full h-48 px-4 py-3 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all duration-200 outline-none resize-none"
                            disabled={loading}
                        />

                        <div className="flex items-center justify-between mt-4">
                            <span className="text-sm text-gray-500">
                                {ticketText.length} characters
                            </span>
                            <div className="flex space-x-3">
                                <button
                                    onClick={handleReset}
                                    disabled={loading || !ticketText}
                                    className="flex items-center space-x-2 px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    <RotateCcw className="w-4 h-4" />
                                    <span>Clear</span>
                                </button>
                                <button
                                    onClick={handlePredict}
                                    disabled={loading || !ticketText}
                                    className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
                                >
                                    {loading ? (
                                        <>
                                            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                                            <span>Analyzing...</span>
                                        </>
                                    ) : (
                                        <>
                                            <Send className="w-4 h-4" />
                                            <span>Predict</span>
                                        </>
                                    )}
                                </button>
                            </div>
                        </div>

                        {/* Example Tickets */}
                        <div className="mt-6">
                            <p className="text-sm font-medium text-gray-700 mb-3">Try an example:</p>
                            <div className="space-y-2">
                                {exampleTickets.map((example, index) => (
                                    <button
                                        key={index}
                                        onClick={() => handleExampleClick(example)}
                                        className="w-full text-left px-3 py-2 text-sm text-gray-700 bg-gray-50 rounded-lg hover:bg-blue-50 hover:text-blue-700 transition-colors"
                                    >
                                        {example}
                                    </button>
                                ))}
                            </div>
                        </div>
                    </motion.div>

                    {/* Results Section */}
                    <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.3 }}
                        className="card"
                    >
                        <div className="flex items-center space-x-2 mb-4">
                            <Target className="w-5 h-5 text-blue-600" />
                            <h2 className="text-xl font-semibold">Prediction Results</h2>
                        </div>

                        {prediction ? (
                            <div className="space-y-4">
                                {/* Category */}
                                <div className="p-4 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl">
                                    <div className="flex items-center justify-between mb-2">
                                        <span className="text-sm font-medium text-gray-600">Category</span>
                                        <span className="text-xs text-gray-500">
                                            {(prediction.category_confidence * 100).toFixed(1)}% confidence
                                        </span>
                                    </div>
                                    <div className={`inline-flex items-center px-4 py-2 bg-gradient-to-r ${getCategoryColor(prediction.category)} text-white rounded-lg font-semibold text-lg`}>
                                        {prediction.category}
                                    </div>
                                    <div className="mt-3 h-2 bg-gray-200 rounded-full overflow-hidden">
                                        <div
                                            className="h-full bg-gradient-to-r from-blue-500 to-indigo-500 transition-all duration-500"
                                            style={{ width: `${prediction.category_confidence * 100}%` }}
                                        ></div>
                                    </div>
                                </div>

                                {/* Priority */}
                                <div className="p-4 bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl">
                                    <div className="flex items-center justify-between mb-2">
                                        <span className="text-sm font-medium text-gray-600">Priority</span>
                                        <span className="text-xs text-gray-500">
                                            {(prediction.priority_confidence * 100).toFixed(1)}% confidence
                                        </span>
                                    </div>
                                    <div className={`inline-flex items-center px-4 py-2 bg-gradient-to-r ${getPriorityColor(prediction.priority)} text-white rounded-lg font-semibold text-lg`}>
                                        {prediction.priority}
                                    </div>
                                    <div className="mt-3 h-2 bg-gray-200 rounded-full overflow-hidden">
                                        <div
                                            className="h-full bg-gradient-to-r from-purple-500 to-pink-500 transition-all duration-500"
                                            style={{ width: `${prediction.priority_confidence * 100}%` }}
                                        ></div>
                                    </div>
                                </div>

                                {/* Metadata */}
                                <div className="grid grid-cols-2 gap-4">
                                    <div className="p-3 bg-gray-50 rounded-lg">
                                        <div className="flex items-center space-x-2 text-gray-600 mb-1">
                                            <Clock className="w-4 h-4" />
                                            <span className="text-xs font-medium">Inference Time</span>
                                        </div>
                                        <p className="text-lg font-semibold text-gray-900">
                                            {prediction.inference_time_ms?.toFixed(0)}ms
                                        </p>
                                    </div>
                                    <div className="p-3 bg-gray-50 rounded-lg">
                                        <div className="flex items-center space-x-2 text-gray-600 mb-1">
                                            <Sparkles className="w-4 h-4" />
                                            <span className="text-xs font-medium">Model</span>
                                        </div>
                                        <p className="text-xs font-semibold text-gray-900">
                                            {prediction.model?.split('/')[1] || 'DeBERTa'}
                                        </p>
                                    </div>
                                </div>

                                {/* Ticket ID */}
                                {prediction.ticket_id && (
                                    <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
                                        <p className="text-xs text-green-700 mb-1">Ticket saved successfully</p>
                                        <p className="text-xs font-mono text-green-900">
                                            ID: {prediction.ticket_id}
                                        </p>
                                    </div>
                                )}
                            </div>
                        ) : (
                            <div className="flex flex-col items-center justify-center h-96 text-center">
                                <div className="w-20 h-20 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-full flex items-center justify-center mb-4">
                                    <TrendingUp className="w-10 h-10 text-blue-600" />
                                </div>
                                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                                    No Prediction Yet
                                </h3>
                                <p className="text-gray-600 max-w-sm">
                                    Enter a ticket description and click "Predict" to see AI-powered classification results
                                </p>
                            </div>
                        )}
                    </motion.div>
                </div>

                {/* Info Cards */}
                <div className="grid md:grid-cols-3 gap-6">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3, delay: 0.1 }}
                        className="card text-center"
                    >
                        <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-3">
                            <Sparkles className="w-6 h-6 text-blue-600" />
                        </div>
                        <h3 className="font-semibold mb-1">AI-Powered</h3>
                        <p className="text-sm text-gray-600">
                            Using DeBERTa transformer model with 184M parameters
                        </p>
                    </motion.div>

                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3, delay: 0.2 }}
                        className="card text-center"
                    >
                        <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3">
                            <Target className="w-6 h-6 text-green-600" />
                        </div>
                        <h3 className="font-semibold mb-1">High Accuracy</h3>
                        <p className="text-sm text-gray-600">
                            99%+ accuracy on ticket classification tasks
                        </p>
                    </motion.div>

                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3, delay: 0.3 }}
                        className="card text-center"
                    >
                        <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-3">
                            <Clock className="w-6 h-6 text-purple-600" />
                        </div>
                        <h3 className="font-semibold mb-1">Lightning Fast</h3>
                        <p className="text-sm text-gray-600">
                            Results in under 200ms with real-time processing
                        </p>
                    </motion.div>
                </div>
            </div>
        </DashboardLayout>
    )
}

export default PredictPage
