import React, { useState, useEffect } from 'react';

export default function App() {
  const [user, setUser] = useState(localStorage.getItem('user') || '');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isRegister, setIsRegister] = useState(false);

  const [activity, setActivity] = useState('');
  const [description, setDescription] = useState('');
  const [city, setCity] = useState('Warszawa');
  const [plannedDate, setPlannedDate] = useState('');
  const [plannedTime, setPlannedTime] = useState('');
  const [editingId, setEditingId] = useState(null);
  const [list, setList] = useState([]);
  const [loading, setLoading] = useState(false);

  const cities = ["Warszawa", "Kraków", "Gdańsk", "Poznań"];

  useEffect(() => {
    fetchActivities();
  }, []);

  const fetchActivities = () => {
    fetch('/activity')
      .then(res => res.json())
      .then(data => setList(data))
      .catch(err => console.error("Błąd pobierania:", err));
  };

  const handleAuth = async (e) => {
    e.preventDefault();
    const endpoint = isRegister ? '/api/register' : '/api/login';
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    const data = await res.json();
    if (data.success) {
      if (!isRegister) {
        setUser(username);
        localStorage.setItem('user', username);
      } else {
        alert("Zarejestrowano! Teraz się zaloguj.");
        setIsRegister(false);
      }
    } else {
      alert(data.error);
    }
  };

  const handleLogout = () => {
    setUser('');
    localStorage.removeItem('user');
  };

  const handleSave = async () => {
    if (!activity) return alert('Wpisz nazwę wyjścia!');
    setLoading(true);

    try {
      const url = editingId ? `/activity/${editingId}` : '/activity';
      const method = editingId ? 'PUT' : 'POST';

      const res = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: user,
          name: activity,
          description,
          city,
          planned_date: plannedDate,
          planned_time: plannedTime
        })
      });
      
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.error || "Błąd serwera");
      }

      setActivity('');
      setDescription('');
      setPlannedDate('');
      setPlannedTime('');
      setEditingId(null);
      fetchActivities();
    } catch (error) {
      alert("Błąd zapisu: " + error.message);
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (item) => {
    setEditingId(item._id);
    setActivity(item.name);
    setDescription(item.description);
    setCity(item.city);
    setPlannedDate(item.planned_date || '');
    setPlannedTime(item.planned_time || '');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const cancelEdit = () => {
    setEditingId(null);
    setActivity('');
    setDescription('');
    setPlannedDate('');
    setPlannedTime('');
  };

  const handleDelete = async (id) => {
    console.log("Próba usunięcia wpisu o ID:", id);
    try {
      const res = await fetch(`/activity/${id}`, {
        method: 'DELETE',
        headers: { 
          'Content-Type': 'application/json',
          'x-username': user
        }
      });
      if (res.ok) {
        console.log("Usunięto pomyślnie");
        fetchActivities();
      } else {
        const data = await res.json();
        console.error("Błąd serwera przy usuwaniu:", data);
        alert(data.error || "Błąd usuwania");
      }
    } catch (err) {
      console.error("Błąd sieci przy usuwaniu:", err);
      alert("Błąd połączenia z serwerem");
    }
  };

  const handleLike = async (id) => {
    await fetch(`/activity/${id}/like`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: user })
    });
    fetchActivities();
  };

  const today = new Date().toISOString().split('T')[0];
  const maxDate = new Date();
  maxDate.setDate(maxDate.getDate() + 13);
  const maxDateStr = maxDate.toISOString().split('T')[0];

  if (!user) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-blue-50">
        <div className="bg-white p-8 rounded-xl shadow-lg w-full max-w-md">
          <h1 className="text-2xl font-bold mb-6 text-center text-blue-600">
            {isRegister ? 'Załóż konto' : 'Zaloguj się'}
          </h1>
          <form onSubmit={handleAuth} className="space-y-4">
            <input 
              type="text" placeholder="Użytkownik" 
              className="w-full border p-3 rounded"
              value={username} onChange={e => setUsername(e.target.value)}
              required
            />
            <input 
              type="password" placeholder="Hasło" 
              className="w-full border p-3 rounded"
              value={password} onChange={e => setPassword(e.target.value)}
              required
            />
            <button className="w-full bg-blue-500 text-white p-3 rounded font-bold hover:bg-blue-600">
              {isRegister ? 'Zarejestruj' : 'Zaloguj'}
            </button>
          </form>
          <p className="mt-4 text-center text-sm text-gray-600">
            {isRegister ? 'Masz już konto?' : 'Nie masz konta?'} 
            <button onClick={() => setIsRegister(!isRegister)} className="ml-1 text-blue-500 underline">
              {isRegister ? 'Zaloguj się' : 'Zarejestruj się'}
            </button>
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8 font-sans max-w-2xl mx-auto bg-gray-50 min-h-screen">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-blue-600">Spotkajmy się;pp</h1>
        <div className="text-right">
          <p className="text-sm text-gray-600">Cześć, <span className="font-bold">{user}</span>!</p>
          <button onClick={handleLogout} className="text-xs text-red-500 underline">Wyloguj</button>
        </div>
      </div>
      
      <div className="bg-white p-6 rounded-xl shadow-md mb-8 border-t-4 border-blue-500">
        <h2 className="font-bold mb-4 text-gray-700">
          {editingId ? 'Edytuj propozycję' : 'Zaplanuj nowe wyjście'}
        </h2>
        <div className="space-y-3">
          <div className="flex gap-2">
            <input 
              type="text" value={activity} onChange={(e) => setActivity(e.target.value)}
              placeholder="Co robimy? (np. Pizza, Kino)"
              className="border p-2 flex-1 rounded"
            />
            <select 
              value={city} onChange={e => setCity(e.target.value)}
              className="border p-2 rounded bg-gray-50"
            >
              {cities.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
            <input 
              type="date" value={plannedDate} onChange={e => setPlannedDate(e.target.value)}
              min={today} max={maxDateStr}
              className="border p-2 rounded bg-gray-50"
            />
            <input 
              type="time" value={plannedTime} onChange={e => setPlannedTime(e.target.value)}
              className="border p-2 rounded bg-gray-50"
            />
          </div>
          <textarea 
            value={description} onChange={e => setDescription(e.target.value)}
            placeholder="Dodatkowy opis (miejsce, godzina...)"
            className="w-full border p-2 rounded h-20"
          />
          <div className="flex gap-2">
            <button 
              onClick={handleSave} disabled={loading}
              className="flex-1 bg-blue-500 text-white py-3 rounded-lg font-bold hover:bg-blue-600 disabled:bg-gray-400"
            >
              {loading ? 'Przetwarzam...' : (editingId ? 'Zapisz zmiany' : 'Dodaj proprozycję')}
            </button>
            {editingId && (
              <button 
                onClick={cancelEdit}
                className="px-4 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
              >
                Anuluj
              </button>
            )}
          </div>
        </div>
      </div>

      <h2 className="text-xl font-semibold mb-4 border-b pb-2">Propozycje wyjść:</h2>
      <div className="space-y-6">
        {list.length === 0 && <p className="text-gray-500 italic text-center">Nikt jeszcze nic nie zaproponował.</p>}
        {list.map((item) => (
          <div key={item._id} className="bg-white p-5 rounded-xl shadow-sm border border-gray-100 relative group">
            <div className="flex justify-between items-start mb-2">
              <div>
                <span className="text-xs font-bold text-blue-500 uppercase tracking-wider">{item.city}</span>
                <h3 className="text-xl font-bold">{item.name}</h3>
                {(item.planned_date || item.planned_time) && (
                  <div className="flex gap-2 mt-1">
                    {item.planned_date && (
                      <span className="bg-blue-50 text-blue-600 px-2 py-0.5 rounded text-xs font-bold inline-block">
                        Data: {item.planned_date}
                      </span>
                    )}
                    {item.planned_time && (
                      <span className="bg-blue-50 text-blue-600 px-2 py-0.5 rounded text-xs font-bold inline-block">
                        Godzina: {item.planned_time}
                      </span>
                    )}
                  </div>
                )}
              </div>
              <div className="text-right">
                <span className="text-xs text-gray-400 block">{new Date(item.timestamp).toLocaleString()}</span>
                <span className="text-sm font-medium text-gray-600">od: {item.username}</span>
              </div>
            </div>

            <p className="text-gray-700 mb-4 whitespace-pre-wrap">{item.description}</p>

            <div className="flex items-center justify-between pt-4 border-t border-gray-50">
              <div className="flex items-center gap-4">
                <button 
                  onClick={() => handleLike(item._id)}
                  className={`flex items-center gap-1 px-3 py-1 rounded-full transition-colors ${item.liked_by.includes(user) ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-500 hover:bg-gray-200'}`}
                >
                  👍 <span className="font-bold">{item.likes_count}</span>
                </button>
                <div className="text-xs text-gray-500">
                  Pogoda: <span className="font-bold">{item.temperature}°C</span>, {item.windspeed} km/h
                  {item.precipitation !== undefined && (
                    <span className="ml-1">
                      | Opady: <span className="font-bold text-blue-500">{item.precipitation} mm</span>
                    </span>
                  )}
                </div>
              </div>
              
              {item.username === user && (
                <div className="flex gap-3">
                  <button 
                    onClick={() => handleEdit(item)}
                    className="text-blue-400 hover:text-blue-600 text-sm"
                  >
                    Edytuj
                  </button>
                  <button 
                    onClick={() => handleDelete(item._id)}
                    className="text-red-400 hover:text-red-600 text-sm"
                  >
                    Usuń
                  </button>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
