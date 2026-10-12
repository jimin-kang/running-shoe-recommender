import React, { useState, useEffect } from "react";

// 1. Define the schema interface for a single object
interface User {
  id: number;
  name: string;
  email: string;
  role: string;
}

export default function UserList() {
  // 2. State typed as an array of the defined schema (User[])
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await fetch("https://example.com");
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data: User[] = await response.json();
        setUsers(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  if (loading) return <div>Loading users...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">User Directory</h2>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {/* 3. Render the array using .map() */}
        {users.map((user) => (
          <div 
            key={user.id} 
            className="border p-4 rounded shadow-sm bg-white"
          >
            <h3 className="font-semibold text-lg">{user.name}</h3>
            <p className="text-gray-600 text-sm">{user.email}</p>
            <span className="inline-block mt-2 px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded">
              {user.role}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
