import { useLocation, useNavigate } from 'react-router-dom';
import RecommendationsList from './RecommendationsList';

/**
 * Component that displays the shoe recommendations
 */
export default function RecommendationsPage() {

  const location = useLocation();
  const navigate = useNavigate();

  // Retrieve the recommendations response passed from the navigate function
  const recommendationsData = location.state?.recommendations;

  if (!recommendationsData) {
    return (
      <div>
        <p>No shoe recommendations found. Please submit your shoe preferences first!</p>
        <button onClick={() => navigate('/')}>Submit your shoe preferences here</button>
      </div>
    );
  }

  return <RecommendationsList recommendations={recommendationsData.recommendations}/>;
}
