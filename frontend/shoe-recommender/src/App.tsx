import './App.css'
import PreferenceSliderForm from './PreferenceSliderForm.tsx'
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import RecommendationsPage from './RecommendationsPage.tsx';


export default function App() {
  return (
    <BrowserRouter>
      <h1>Welcome to your own shoe recommender :) </h1>
      <Routes>
        <Route path="/" element={<PreferenceSliderForm />} />
        <Route path="/recommendations" element={<RecommendationsPage />} />
      </Routes>
    </BrowserRouter>
  );
}
