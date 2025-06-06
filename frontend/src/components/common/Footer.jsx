const Footer = () => {
  const currentYear = new Date().getFullYear();
  return (
    <footer className="bg-gray-50 border-t border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-wider">
              Text Summarization Tool
            </h3>
            <p className="mt-2 text-sm text-gray-600">
              AI-powered text summarization for documents and articles.
            </p>
          </div>
          <div>
            <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-wider">
              Features
            </h3>
            <ul className="mt-2 space-y-1">
              <li><span className="text-sm text-gray-600">Extractive Summarization</span></li>
              <li><span className="text-sm text-gray-600">Document Upload</span></li>
              <li><span className="text-sm text-gray-600">Multiple Formats</span></li>
              <li><span className="text-sm text-gray-600">User Feedback</span></li>
            </ul>
          </div>
          <div>
            <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-wider">
              Support
            </h3>
            <ul className="mt-2 space-y-1">
              <li><span className="text-sm text-gray-600">Documentation</span></li>
              <li><span className="text-sm text-gray-600">API Reference</span></li>
              <li><span className="text-sm text-gray-600">Contact Support</span></li>
            </ul>
          </div>
        </div>
        <div className="mt-8 pt-8 border-t border-gray-200">
          <p className="text-sm text-gray-400 text-center">
            © {currentYear} Text Summarization Tool. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

