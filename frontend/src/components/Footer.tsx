import { Github, Twitter } from "lucide-react";

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-900 p-4 fixed bottom-0 left-0 right-0 flex justify-center gap-8">
      <a
        href="https://twitter.com"
        target="_blank"
        rel="noopener noreferrer"
        className="text-white hover:text-blue-500 transition"
      >
        <Twitter size={24} />
      </a>
      <a
        href="https://github.com"
        target="_blank"
        rel="noopener noreferrer"
        className="text-white hover:text-gray-400 transition"
      >
        <Github size={24} />
      </a>
    </footer>
  );
};

export default Footer;