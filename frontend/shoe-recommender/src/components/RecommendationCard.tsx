import type {RecommendationCardProps} from "@/types";

/**
 * Helper to display the value with the specified unit.
 * @param value 
 * @param unit 
 * @returns 
 */
function formatSpec(
  value: number | null,
  unit: string,
): string {
  return value == null ? "N/A" : `${value} ${unit}`;
}

/**
 * Result card to display a single shoe recommendation.
 * @param recommendation: the shoe recommendation
 * @returns 
 */
export default function RecommendationCard({
  recommendation,
}: RecommendationCardProps) {
  const { shoe, score, reasons } = recommendation;

  const scorePercent = Math.round(score * 100);

  return (
    <article className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm transition-shadow hover:shadow-md dark:border-gray-700 dark:bg-gray-900 sm:p-6">
      {/* Header */}
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <p className="text-sm font-medium uppercase tracking-wider text-gray-500">
            {shoe.brand}
          </p>

          <h2 className="mt-1 text-xl font-bold text-gray-900 dark:text-white sm:text-2xl">
            {shoe.model}
          </h2>

          <p className="mt-2 text-sm capitalize text-gray-500">
            {shoe.use_case} running · {shoe.terrain}
          </p>
        </div>

        {/* Highlighted recommendation score */}
        <div className="shrink-0 rounded-xl bg-emerald-50 px-4 py-3 text-center dark:bg-emerald-950">
          <p className="text-2xl font-bold text-emerald-700 dark:text-emerald-300">
            {scorePercent}%
          </p>
          <p className="text-xs font-medium text-emerald-700 dark:text-emerald-300">
            Match score
          </p>
        </div>
      </div>

      {/* Physical specifications */}
      <div className="my-5 grid grid-cols-2 gap-3 sm:grid-cols-4">
        {[
          {
            label: "Weight",
            value: formatSpec(shoe.weight_g, "g"),
          },
          {
            label: "Heel stack",
            value: formatSpec(shoe.heel_stack_mm, "mm"),
          },
          {
            label: "Forefoot stack",
            value: formatSpec(shoe.forefoot_stack_mm, "mm"),
          },
          {
            label: "Heel-to-toe drop",
            value: formatSpec(shoe.drop_mm, "mm"),
          },
        ].map((spec) => (
          <div
            key={spec.label}
            className="rounded-lg bg-gray-50 p-3 dark:bg-gray-800"
          >
            <p className="text-xs text-gray-500">
              {spec.label}
            </p>
            <p className="mt-1 font-semibold text-gray-900 dark:text-white">
              {spec.value}
            </p>
          </div>
        ))}
      </div>

      {/* Recommendation reasons */}
      <div className="border-t border-gray-100 pt-4 dark:border-gray-700">
        <h3 className="font-semibold text-gray-900 dark:text-white">
          Why you&apos;ll like it
        </h3>

        {reasons.length > 0 ? (
          <ul className="mt-3 space-y-2">
            {reasons.map((reason, index) => (
              <li
                key={`${index}-${reason}`}
                className="flex items-start gap-2 text-sm leading-6 text-gray-600 dark:text-gray-300"
              >
                <span
                  aria-hidden="true"
                  className="mt-1 flex size-5 shrink-0 items-center justify-center rounded-full bg-emerald-100 text-xs text-emerald-700 dark:bg-emerald-900 dark:text-emerald-300"
                >
                  ✓
                </span>
                <span>{reason}</span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="mt-2 text-sm text-gray-500">
            No recommendation reasons available.
          </p>
        )}
      </div>
    </article>
  );
}