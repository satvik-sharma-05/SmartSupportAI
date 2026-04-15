import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';

const HomePage = () => {
    const features = [
        {
            icon: (
                <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
            ),
            title: 'Intelligent Classification',
            description: 'AI-powered ticket categorization with 85%+ accuracy using advanced transformer models'
        },
        {
            icon: (
                <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
            ),
            title: 'Priority Detection',
            description: 'Automatically identify urgent tickets and route them to the right team instantly'
        },
        {
            icon: (
                <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
            ),
            title: 'Real-time Analytics',
            description: 'Get instant insights into ticket trends, categories, and team performance'
        },
        {
            icon: (
                <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
            ),
            title: 'Lightning Fast',
            description: 'Process thousands of tickets in seconds with our optimized AI pipeline'
        },
        {
            icon: (
                <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
            ),
            title: 'Enterprise Security',
            description: 'Bank-level encryption and compliance with SOC 2, GDPR, and HIPAA standards'
        },
        {
            icon: (
                <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z" />
                </svg>
            ),
            title: 'Easy Integration',
            description: 'Connect with your existing tools via REST API, webhooks, or native integrations'
        }
    ];

    return (
        <div className="min-h-screen">
            <Navbar />

            {/* Hero Section */}
            <section className="relative pt-32 pb-20 px-4 overflow-hidden">
                {/* Animated background blobs */}
                <div className="absolute inset-0 overflow-hidden pointer-events-none">
                    <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary-500/20 rounded-full blur-3xl animate-float"></div>
                    <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-accent-purple/20 rounded-full blur-3xl animate-float" style={{ animationDelay: '1s' }}></div>
                </div>

                <div className="max-w-7xl mx-auto relative z-10">
                    <div className="text-center space-y-8 animate-fade-in">
                        <h1 className="text-5xl md:text-7xl font-display font-bold leading-tight">
                            <span className="gradient-text">AI-Powered</span>
                            <br />
                            Support Ticket Intelligence
                        </h1>

                        <p className="text-xl md:text-2xl text-dark-300 max-w-3xl mx-auto">
                            Transform your customer support with intelligent ticket classification,
                            priority detection, and real-time insights powered by advanced AI
                        </p>

                        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
                            <Link to="/signup" className="btn-primary text-lg px-8 py-4">
                                Get Started Free
                                <svg className="w-5 h-5 ml-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                                </svg>
                            </Link>
                            <Link to="/predict" className="btn-secondary text-lg px-8 py-4">
                                Try Demo
                            </Link>
                        </div>

                        {/* Stats */}
                        <div className="grid grid-cols-3 gap-8 pt-12 max-w-3xl mx-auto">
                            <div className="text-center">
                                <div className="text-4xl font-bold gradient-text">85%+</div>
                                <div className="text-dark-400 mt-1">Accuracy</div>
                            </div>
                            <div className="text-center">
                                <div className="text-4xl font-bold gradient-text">&lt;200ms</div>
                                <div className="text-dark-400 mt-1">Response Time</div>
                            </div>
                            <div className="text-center">
                                <div className="text-4xl font-bold gradient-text">24/7</div>
                                <div className="text-dark-400 mt-1">Availability</div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="py-20 px-4">
                <div className="max-w-7xl mx-auto">
                    <div className="text-center mb-16 animate-slide-up">
                        <h2 className="text-4xl md:text-5xl font-display font-bold mb-4">
                            Powerful Features
                        </h2>
                        <p className="text-xl text-dark-300">
                            Everything you need to supercharge your support team
                        </p>
                    </div>

                    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {features.map((feature, index) => (
                            <div
                                key={index}
                                className="card-premium group hover:scale-105 cursor-pointer animate-slide-up"
                                style={{ animationDelay: `${index * 0.1}s` }}
                            >
                                <div className="text-primary-400 mb-4 transform group-hover:scale-110 transition-transform duration-300">
                                    {feature.icon}
                                </div>
                                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                                <p className="text-dark-400">{feature.description}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* How It Works */}
            <section className="py-20 px-4">
                <div className="max-w-5xl mx-auto">
                    <div className="text-center mb-16">
                        <h2 className="text-4xl md:text-5xl font-display font-bold mb-4">
                            How It Works
                        </h2>
                        <p className="text-xl text-dark-300">
                            Three simple steps to intelligent support
                        </p>
                    </div>

                    <div className="grid md:grid-cols-3 gap-8">
                        {[
                            { step: '01', title: 'Input Ticket', desc: 'Submit your support ticket text' },
                            { step: '02', title: 'AI Processing', desc: 'Our AI analyzes and classifies' },
                            { step: '03', title: 'Get Results', desc: 'Receive category and priority instantly' }
                        ].map((item, index) => (
                            <div key={index} className="text-center">
                                <div className="w-20 h-20 mx-auto mb-4 bg-gradient-to-br from-primary-500 to-accent-purple rounded-2xl flex items-center justify-center text-3xl font-bold">
                                    {item.step}
                                </div>
                                <h3 className="text-2xl font-semibold mb-2">{item.title}</h3>
                                <p className="text-dark-400">{item.desc}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-20 px-4">
                <div className="max-w-4xl mx-auto">
                    <div className="card-premium text-center p-12 bg-gradient-to-br from-primary-600/20 to-accent-purple/20">
                        <h2 className="text-4xl md:text-5xl font-display font-bold mb-4">
                            Ready to Transform Your Support?
                        </h2>
                        <p className="text-xl text-dark-300 mb-8">
                            Join thousands of teams using SmartSupport AI
                        </p>
                        <Link to="/signup" className="btn-primary text-lg px-8 py-4 inline-flex items-center">
                            Start Using SmartSupport AI
                            <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                            </svg>
                        </Link>
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="border-t border-white/10 py-8 px-4">
                <div className="max-w-7xl mx-auto text-center text-dark-400">
                    <p>&copy; 2024 SmartSupport AI. All rights reserved.</p>
                </div>
            </footer>
        </div>
    );
};

export default HomePage;
