import React, { useState } from 'react';

export default function NumberSliderForm() {
    // Weight preference
  const [weight, setWeight] = useState<number>();
  const handleWeightSliderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setWeight(Number(e.target.value));
  };
  const handleWeightInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value === '' ? 0 : Number(e.target.value);
    setWeight(val);
  };

  // Forefoot Stack preference
  const [forefootStack, setForefootStack] = useState<number>();
  const handleForefootSliderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForefootStack(Number(e.target.value));
  };
  const handleForefootInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value === '' ? 0 : Number(e.target.value);
    setForefootStack(val);
  };

  // Heel Stack preference
  const [heelStack, setHeelStack] = useState<number>();
  const handleHeelSliderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setHeelStack(Number(e.target.value));
  };
  const handleHeelInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value === '' ? 0 : Number(e.target.value);
    setHeelStack(val);
  };

  // Submit handler to call the recommendation API 
  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault(); // Stop default browser page refresh

    // setStatus('Submitting...');
    const RECOMMENDATION_API = "http://localhost:8000/api/recommendations"
    try {
      // 2. Make the API call
      const response = await fetch(RECOMMENDATION_API, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            "weight": weight,
            "weight_importance": 1,
            "forefoot_stack": forefootStack,
            "forefoot_stack_importance": 1,
            "heel_stack": heelStack,
            "heel_stack_importance": 1,
            "plated": true,
            "plated_constraint": true
        }), // TODO: send preference form as request body
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      console.log("RECOMMENDATIONS:\n", JSON.stringify(data, null, 2))
      console.log('Successfully fetched recommendations!');
    } catch (error) {
      console.log('Error submitting shoe preferences :(');
    }
  }
  

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem', maxWidth: '300px' }}>
      <label htmlFor="range-slider">Weight (g): {weight}</label>
      <input
        id="range-slider"
        type="range"
        min={100}
        max={400}
        step={1}
        value={weight}
        onChange={handleWeightSliderChange}
      />
      <input
        type="number"
        min={100}
        max={400}
        value={weight}
        onChange={handleWeightInputChange}
      />

      <label htmlFor="range-slider">Forefoot Stack (mm): {forefootStack}</label>
      <input
        id="range-slider"
        type="range"
        min={0}
        max={50}
        step={1}
        value={forefootStack}
        onChange={handleForefootSliderChange}
      />
      <input
        type="number"
        min={0}
        max={50}
        value={forefootStack}
        onChange={handleForefootInputChange}
      />

      <label htmlFor="range-slider">Heel Stack (mm): {heelStack}</label>
      <input
        id="range-slider"
        type="range"
        min={0}
        max={50}
        step={1}
        value={heelStack}
        onChange={handleHeelSliderChange}
      />
      <input
        type="number"
        min={0}
        max={100}
        value={heelStack}
        onChange={handleHeelInputChange}
      />

      <button type="submit">Get Recommendations</button>
    </form>
  );
}
