import Logo from "./Logo";

const Header: React.FC = () => {
  return (
    <header className="bg-gray-900 p-4 flex justify-between items-center shadow-md">
      <Logo />
    </header>
  );
};

export default Header;