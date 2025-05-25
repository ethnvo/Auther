import SearchBar from "../components/SearchBar";

export default function HomePage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-white px-4">
      <h1 className="text-5xl font-bold text-indigo-600 mb-12">auther</h1>
      <SearchBar autoFocus placeholder="Search academic topics..." />
    </div>
  );
}
