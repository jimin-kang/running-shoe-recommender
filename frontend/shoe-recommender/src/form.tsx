import React, { useState, type ChangeEvent, type FormEvent } from 'react';

export default function InputFormPage() {
  // 1. Declare state for the input value
  const [inputValue, setInputValue] = useState<string>('');
  const [submittedValue, setSubmittedValue] = useState<string>('');

  // 2. Handle input changes with proper TypeScript typing
  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    console.log("change event, setting input value: ", e.target.value);
    setInputValue(e.target.value);
  };

  // 3. Handle form submission
  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault(); // Prevent page reload
    setSubmittedValue(inputValue);
    setInputValue(''); // Clear input if needed
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Simple Input Form</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="userInput">Enter text: </label>
          <input
            id="userInput"
            type="text"
            value={inputValue}
            onChange={handleChange}
            placeholder="Type something..."
          />
        </div>
        <button type="submit" style={{ marginTop: '10px' }}>
          Submit
        </button>
      </form>

      {submittedValue && (
        <p style={{ marginTop: '20px' }}>
          You entered: <strong>{submittedValue}</strong>
        </p>
      )}
    </div>
  );
}
