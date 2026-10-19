
import RecommendationCard from "@/components/RecommendationCard";
import type {ShoeRecommendation} from "@/types"

type RecommendationsListProps = {
  recommendations: ShoeRecommendation[];
};

/**
 * Component that displays all the shoe recommendations
 * @param recommendations: List of shoe recommendations
 * @returns 
 */
export default function RecommendationsList({
  recommendations,
}: RecommendationsListProps) {
  if (recommendations.length === 0) {
    return (
      <p className="py-12 text-center text-gray-500">
        No matching shoes found. Try adjusting your preferences.
      </p>
    );
  }

  return (
    <section className="mx-auto max-w-4xl space-y-5">
      <div>
        <h1 className="text-2xl font-bold">
          Your Recommendations
        </h1>
        <p className="mt-1 text-sm text-gray-500">
          Shoes ranked by how closely they match your preferences.
        </p>
      </div>

      {recommendations.map((recommendation) => (
        <RecommendationCard
          key={recommendation.shoe.id}
          recommendation={recommendation}
        />
      ))}
    </section>
  );
}