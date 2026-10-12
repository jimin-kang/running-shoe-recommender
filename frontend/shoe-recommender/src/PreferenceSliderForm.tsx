import './PreferenceSliderForm.css'
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'
import { RECOMMENDATION_API } from './constants';

/**
 * Component to accept shoe preferences.
 * 
 * Input form for shoe preferences should include:
 * - Physical specs: weight, stack height, etc.
 * - Constraints: plate/no-plate
 * - Qualitative stuff: use-case, durability, etc.   
 * @returns 
 */
export default function PreferenceSliderForm() {

  // PHYSICAL SPECS
  // Weight
  const [weight, setWeight] = useState<number>(0);
  const [weightImportance, setWeightImportance] = useState<number>(0.5);

  // Forefoot Stack preference
  const [forefootStack, setForefootStack] = useState<number>(0);
  const [forefootStackImportance, setForefootStackImportance] = useState<number>(0.5);

  // Heel Stack preference
  const [heelStack, setHeelStack] = useState<number>(0);
  const [heelStackImportance, setHeelStackImportance] = useState<number>(0.5);

  // Hook to navigate between routes based on user events
  const navigate = useNavigate();

  /**
   * Event handler called when user submits their preferences.
   * Calls the recommendation API and redirects the user to the recommendation page.
   * @param e 
   */
  async function handleSubmit(e: React.SubmitEvent<HTMLFormElement>) {
    e.preventDefault(); // Stop default browser page refresh

    try {
      // Make the API call
      const response = await fetch(
        RECOMMENDATION_API,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            "weight": weight,
            "weight_importance": weightImportance,
            "forefoot_stack": forefootStack,
            "forefoot_stack_importance": forefootStackImportance,
            "heel_stack": heelStack,
            "heel_stack_importance": heelStackImportance,
            "plated": true,
            "plated_constraint": true
          }),
        }
      );

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      console.log("RECOMMENDATIONS:\n", JSON.stringify(data, null, 2))

      // Navigate and pass the response data into the router state
      navigate(
        "/recommendations",
        { state: { recommendations: data } }
      );

    } catch (error) {
      console.log('Error submitting shoe preferences :(');
    }
  }


  return (
    <div className="preference-form-wrapper">

      <form className="preference-form" onSubmit={handleSubmit}>
        <table className="preference-form-table">
          <tbody>
            {/* Row 1: Weight */}
            <tr>
              <td>
                <div className="preference-form-cell">
                  <div className="preference-form-cell-label">
                    <label htmlFor="weight-range-slider">Weight (g): {weight}</label>
                  </div>
                  <div className="preference-form-cell-slider">
                    <input
                      id="weight-range-slider"
                      type="range"
                      min={100}
                      max={400}
                      step={1}
                      value={weight}
                      onChange={(e) => setWeight(Number(e.target.value))}
                    />
                  </div>
                  <div className="preference-form-cell-input">
                    <input
                      type="number"
                      min={100}
                      max={400}
                      value={weight}
                      onChange={(e) => setWeight(Number(e.target.value))}
                    />
                  </div>
                </div>
              </td>
              <td>
                <div className="preference-form-cell">
                  <div className="preference-form-cell-label">
                    <label htmlFor="weight-importance-range-slider">Weight Importance</label>
                  </div>
                  <div className="preference-form-cell-slider">
                    <input
                      id="weight-importance-range-slider"
                      type="range"
                      min={0}
                      max={1}
                      step={0.01}
                      value={weightImportance}
                      onChange={e => setWeightImportance(Number(e.target.value))}
                    />
                  </div>
                  <div className="preference-form-cell-input">
                    <input
                      type="number"
                      min={0}
                      max={1}
                      step={0.01}
                      placeholder={0.5}
                      value={weightImportance}
                      onChange={e => setWeightImportance(Number(e.target.value))}
                    />
                  </div>
                </div>
              </td>
            </tr>

            {/* Row 2: Forefoot stack */}
            <tr>
              <td>
                <div className="preference-form-cell">
                  <div className="preference-form-cell-label">
                    <label htmlFor="forefoot-stack-range-slider">Forefoot Stack (mm): {forefootStack}</label>
                  </div>
                  <div className="preference-form-cell-slider">
                    <input
                      id="forefoot-stack-range-slider"
                      type="range"
                      min={0}
                      max={50}
                      step={1}
                      value={forefootStack}
                      onChange={e => setForefootStack(Number(e.target.value))}
                    />
                  </div>
                  <div className="preference-form-cell-input">
                    <input
                      type="number"
                      min={0}
                      max={50}
                      value={forefootStack}
                      onChange={e => setForefootStack(Number(e.target.value))}
                    />
                  </div>
                </div>
              </td>
              <td>
                <div className="preference-form-cell">
                  <div className="preference-form-cell-label">
                    <label htmlFor="forefoot-stack-importance-range-slider">Forefoot Stack Importance</label>
                  </div>
                  <div className="preference-form-cell-slider">
                    <input
                      id="forefoot-stack-importance-range-slider"
                      type="range"
                      min={0}
                      max={1}
                      step={0.01}
                      value={forefootStackImportance}
                      onChange={e => setForefootStackImportance(Number(e.target.value))}
                    />
                  </div>
                  <div className="preference-form-cell-input">
                    <input
                      type="number"
                      min={0}
                      max={1}
                      step={0.01}
                      placeholder={0.5}
                      value={forefootStackImportance}
                      onChange={e => setForefootStackImportance(Number(e.target.value))}
                    />
                  </div>
                </div>
              </td>
            </tr>

            {/* Row 3: Heel Stack */}
            <tr>
              <td>
                <div className="preference-form-cell">
                  <div className="preference-form-cell-label">
                    <label htmlFor="heel-stack-range-slider">Heel Stack (mm): {heelStack}</label>
                  </div>
                  <div className="preference-form-cell-slider">
                    <input
                      id="heel-stack-range-slider"
                      type="range"
                      min={0}
                      max={50}
                      step={1}
                      value={heelStack}
                      onChange={e => setHeelStack(Number(e.target.value))}
                    />
                  </div>
                  <div className="preference-form-cell-input">
                    <input
                      type="number"
                      min={0}
                      max={100}
                      value={heelStack}
                      onChange={e => setHeelStack(Number(e.target.value))}
                    />
                  </div>
                </div>
              </td>
              <td>
                <div className="preference-form-cell">
                  <div className="preference-form-cell-label">
                    <label htmlFor="heel-stack-importance-range-slider">Heel Stack Importance</label>
                  </div>
                  <div className="preference-form-cell-slider">
                    <input
                      id="heel-stack-importance-range-slider"
                      type="range"
                      min={0}
                      max={1}
                      step={0.01}
                      value={heelStackImportance}
                      onChange={e => setHeelStackImportance(Number(e.target.value))}
                    />
                  </div>
                  <div className="preference-form-cell-input">
                    <input
                      type="number"
                      min={0}
                      max={1}
                      step={0.01}
                      placeholder={0.5}
                      value={heelStackImportance}
                      onChange={e => setHeelStackImportance(Number(e.target.value))}
                    />
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        <button type="submit">Get Recommendations</button>
      </form>
    </div>
  );
}
