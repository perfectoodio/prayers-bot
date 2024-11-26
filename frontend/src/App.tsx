import Header from "./components/Header";
import PrayerForm from "./components/PrayerForm";
import Footer from "./components/Footer";

const App: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Header />
      <main className="container mx-auto px-4 pb-16">
        <PrayerForm />
      </main>
      <Footer />
    </div>
  );
};

export default App;
