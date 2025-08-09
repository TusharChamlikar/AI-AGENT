import React from 'react';
import { Link } from 'react-router-dom';

// --- SVG Icon Components ---
const ChatIcon = () => (
    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a2 2 0 01-2-2V7a2 2 0 012-2h6l2-2h2l-2 2z"></path></svg>
);
const CalendarIcon = () => (
    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
);
// NEW Phone Icon
const PhoneIcon = () => (
    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path></svg>
);
// NEW SMS Icon
const SmsIcon = () => (
    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg>
);
const ArrowRightIcon = () => (
     <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
);

// --- Reusable Components ---
const CtaButton = ({ to, children, primary = false }) => {
    const baseClasses = "cta-button font-bold px-8 py-4 rounded-lg text-lg";
    const primaryClasses = "bg-indigo-600 text-white hover:bg-indigo-700";
    const secondaryClasses = "bg-white text-gray-800 hover:bg-gray-50";
    
    if (to.startsWith('#')) {
        return (
            <a href={to} className={`${baseClasses} ${primary ? primaryClasses : secondaryClasses}`}>
                {children}
            </a>
        );
    }
    
    return (
        <Link to={to} className={`${baseClasses} ${primary ? primaryClasses : secondaryClasses}`}>
            {children}
        </Link>
    );
};

const FeatureCard = ({ icon, title, children }) => (
    <div className="feature-card bg-gray-50 p-8 rounded-xl shadow-sm">
        <div className="bg-indigo-100 text-indigo-600 rounded-full h-12 w-12 flex items-center justify-center mb-4">
            {icon}
        </div>
        <h4 className="text-xl font-bold mb-2">{title}</h4>
        <p className="text-gray-600">{children}</p>
    </div>
);

// --- Section Components ---
const Header = () => (
    <header className="fixed w-full bg-white bg-opacity-80 backdrop-blur-md z-50 shadow-sm">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900">
                Fin-Minder <span className="text-indigo-500">.</span>
            </h1>
            <nav className="hidden md:flex items-center space-x-8">
                <a href="#features" className="text-gray-600 hover:text-indigo-600 transition">Features</a>
                <a href="#how-it-works" className="text-gray-600 hover:text-indigo-600 transition">How It Works</a>
                <a href="#tech-stack" className="text-gray-600 hover:text-indigo-600 transition">Tech Stack</a>
            </nav>
            <div className="flex items-center space-x-4">
                 <a href="#demo" className="cta-button bg-indigo-600 text-white font-semibold px-5 py-2 rounded-lg hover:bg-indigo-700">
                    Watch Demo
                </a>
            </div>
        </div>
    </header>
);

const HeroSection = () => (
    <section id="home" className="gradient-bg pt-32 pb-20">
        <div className="container mx-auto px-6 text-center">
            <div className="max-w-3xl mx-auto">
                <p className="text-indigo-600 font-semibold mb-2">Swafinix AI Hackathon 2025: Finance & Banking</p>
                <h2 className="text-4xl md:text-6xl font-extrabold text-gray-900 mb-4 leading-tight">
                    Never Miss a Payment with an <span className="hero-gradient-text">AI Voice Agent</span>
                </h2>
                <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
                    Fin-Minder is an intelligent, automated voice agent that sends friendly, personalized payment reminders, reducing late fees and improving cash flow for businesses.
                </p>
                <div className="flex justify-center items-center space-x-4">
                    <CtaButton to="/add-reminder" primary>See it in Action</CtaButton>
                    <CtaButton to="#tech-stack">View Tech Stack</CtaButton>
                </div>
            </div>
        </div>
    </section>
);

// --- MODIFIED SECTION ---
const FeaturesSection = () => (
    <section id="features" className="py-20 bg-white">
        <div className="container mx-auto px-6">
            <div className="text-center mb-12">
                <h3 className="text-3xl md:text-4xl font-bold text-gray-900">Why Fin-Minder is a Game-Changer</h3>
                <p className="text-gray-600 mt-2">Automate, personalize, and streamline your payment collections.</p>
            </div>
            {/* Updated to a 2x2 grid on medium screens and up */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
                <FeatureCard icon={<ChatIcon />} title="Conversational AI Voice">
                    Utilizes state-of-the-art text-to-speech for natural, human-like conversations that don't feel robotic.
                </FeatureCard>
                <FeatureCard icon={<CalendarIcon />} title="Smart Scheduling">
                    Intelligently schedules reminder calls at optimal times, increasing the likelihood of reaching the customer.
                </FeatureCard>
                <FeatureCard icon={<SmsIcon />} title="Automated SMS and Email Reminders">
                    Send timely and effective SMS and Email alerts directly to customers, ensuring they never miss a payment due date.
                </FeatureCard>
                <FeatureCard icon={<PhoneIcon />} title="Personalized Call Reminders">
                    Go beyond text with automated, friendly voice calls that provide a personal touch and capture attention.
                </FeatureCard>
            </div>
        </div>
    </section>
);
// --- END OF MODIFICATION ---

const HowItWorksSection = () => (
    <section id="how-it-works" className="py-20 bg-gray-50">
        <div className="container mx-auto px-6">
            <div className="text-center mb-12">
                <h3 className="text-3xl md:text-4xl font-bold text-gray-900">Simple Setup, Powerful Results</h3>
                <p className="text-gray-600 mt-2">Launch your AI agent in three simple steps.</p>
            </div>
            <div className="flex flex-col md:flex-row justify-center items-center gap-8 md:gap-16">
                <div className="text-center max-w-xs">
                    <div className="bg-indigo-600 text-white rounded-full h-16 w-16 flex items-center justify-center text-2xl font-bold mx-auto mb-4">1</div>
                    <h4 className="text-xl font-bold mb-2">Connect Data</h4>
                    <p className="text-gray-600">Securely link your customer and invoice data from your existing CRM or database.</p>
                </div>
                <div className="hidden md:block text-gray-300"><ArrowRightIcon /></div>
                <div className="text-center max-w-xs">
                    <div className="bg-indigo-600 text-white rounded-full h-16 w-16 flex items-center justify-center text-2xl font-bold mx-auto mb-4">2</div>
                    <h4 className="text-xl font-bold mb-2">Configure Agent</h4>
                    <p className="text-gray-600">Customize the AI's voice, script, and calling logic using our no-code workflow designer.</p>
                </div>
                <div className="hidden md:block text-gray-300"><ArrowRightIcon /></div>
                <div className="text-center max-w-xs">
                    <div className="bg-indigo-600 text-white rounded-full h-16 w-16 flex items-center justify-center text-2xl font-bold mx-auto mb-4">3</div>
                    <h4 className="text-xl font-bold mb-2">Go Live</h4>
                    <p className="text-gray-600">Activate your agent and watch as it autonomously handles payment reminders and updates your records.</p>
                </div>
            </div>
        </div>
    </section>
);

const DemoSection = () => (
    <section id="demo" className="py-20 bg-white">
        <div className="container mx-auto px-6">
            <div className="bg-indigo-600 rounded-2xl p-8 md:p-16 text-center shadow-2xl">
                <h3 className="text-3xl md:text-4xl font-bold text-white mb-4">Watch the AI Agent in Action</h3>
                <p className="text-indigo-200 mb-8 max-w-2xl mx-auto">This video demonstrates the entire workflow, from the AI initiating the call to successfully processing a payment reminder.</p>
                
                <div className="max-w-3xl mx-auto bg-gray-900 rounded-lg overflow-hidden shadow-lg aspect-video">
                    <iframe 
                        className="w-full h-full"
                        src="https://www.youtube.com/embed/joMKRnmgq20?si=w17TQuQe-gckxxgr"
                        title="YouTube video player" 
                        frameBorder="0" 
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                        allowFullScreen>
                    </iframe>
                </div>

            </div>
        </div>
    </section>
);

const TechStackSection = () => (
    <section id="tech-stack" className="py-20 bg-gray-50">
        <div className="container mx-auto px-6">
            <div className="text-center mb-12">
                <h3 className="text-3xl md:text-4xl font-bold text-gray-900">Built with Cutting-Edge Technology</h3>
                <p className="text-gray-600 mt-2">We've used industry-leading tools to create a robust and scalable solution.</p>
            </div>
            <div className="max-w-4xl mx-auto">
                <div className="flex flex-wrap justify-center items-center gap-x-8 gap-y-6 md:gap-x-12">
                    
                    <img src="https://placehold.co/120x50/ffffff/333333?text=Twilio" alt="Twilio Logo" className="h-10 md:h-12" />
                    <img src="https://placehold.co/120x50/ffffff/333333?text=SendGrid" alt="SendGrid AI Logo" className="h-10 md:h-12" />
                      {/* <img src="https://placehold.co/120x50/ffffff/333333?text=AWS" alt="AWS Logo" className="h-12 md:h-14" /> */}
                      <img src="https://placehold.co/120x50/ffffff/333333?text=Python" alt="Python" className="h-10 md:h-12" />
                      <img src="https://placehold.co/120x50/ffffff/333333?text=React" alt="React" className="h-10 md:h-12" />
                    <img src="https://placehold.co/120x50/ffffff/333333?text=ElevenLabs" alt="ElevenLabs Logo" className="h-12 md:h-14" />
                    
                  
                    <img src="https://placehold.co/120x50/ffffff/333333?text=OpenAI" alt="OpenAI Logo" className="h-12 md:h-14" />
                </div>
            </div>
        </div>
    </section>
);

const Footer = () => (
    <footer className="bg-gray-900 text-white">
        <div className="container mx-auto px-6 py-8 text-center">
            <p>© 2025 Fin-Minder. A project for the Swafinix AI Hackathon.</p>
            <p className="text-gray-400 text-sm mt-2">Built with passion by Team Swafinix.</p>
        </div>
    </footer>
);

// --- Main HomePage Component ---
export default function HomePage() {
    return (
        <>
            <style>{`
                html {
                    scroll-behavior: smooth;
                }
                body {
                    font-family: 'Inter', sans-serif;
                }
                .gradient-bg {
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                }
                .hero-gradient-text {
                    background: -webkit-linear-gradient(45deg, #3b82f6, #8b5cf6);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                }
                .cta-button {
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 6px rgba(50, 50, 93, 0.11), 0 1px 3px rgba(0, 0, 0, 0.08);
                }
                .cta-button:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 7px 14px rgba(50, 50, 93, 0.1), 0 3px 6px rgba(0, 0, 0, 0.08);
                }
                .feature-card {
                    transition: all 0.3s ease;
                }
                .feature-card:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
                }
            `}</style>
            <div className="bg-white text-gray-800">
                <Header />
                <main>
                    <HeroSection />
                    <FeaturesSection />
                    <HowItWorksSection />
                    <DemoSection />
                    <TechStackSection />
                </main>
                <Footer />
            </div>
        </>
    );
}
