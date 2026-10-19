import './App.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import ShoePreferenceForm from '@/pages/ShoePreferenceForm.tsx'
import RecommendationsPage from '@/pages/RecommendationsPage.tsx';
import NotFound from '@/pages/NotFound.tsx';


export default function App() {
  return (
    <BrowserRouter>
      <h1>Welcome to your own shoe recommender :) </h1>

      {/* Load the preference form or the recommendation page according to the URL */}
      <Routes>
        <Route path="/" element={<ShoePreferenceForm />} />
        <Route path="/recommendations" element={<RecommendationsPage />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}
