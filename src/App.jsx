import React, { useState, useEffect, useMemo } from 'react';
import courseData from './data.json';
import { Download, Save, BookOpen, FileText, Users, Activity, FileDigit, Trash2, FolderOpen } from 'lucide-react';

const App = () => {
  const [selectedClass, setSelectedClass] = useState('');
  const [selectedChapters, setSelectedChapters] = useState(new Set());
  const [savedCollections, setSavedCollections] = useState([]);
  const [collectionName, setCollectionName] = useState('');
  const [showSaveModal, setShowSaveModal] = useState(false);

  // Load saved collections from local storage
  useEffect(() => {
    const saved = localStorage.getItem('coursePlannerCollections');
    if (saved) {
      setSavedCollections(JSON.parse(saved));
    }
  }, []);

  const chapters = useMemo(() => {
    if (!selectedClass) return [];
    return courseData.chapters.filter(c => c.class.includes(selectedClass));
  }, [selectedClass]);

  const toggleChapter = (id) => {
    const newSet = new Set(selectedChapters);
    if (newSet.has(id)) {
      newSet.delete(id);
    } else {
      newSet.add(id);
    }
    setSelectedChapters(newSet);
  };

  const generatePlan = useMemo(() => {
    const plan = [];
    const selectedChaps = courseData.chapters.filter(c => selectedChapters.has(c.id));

    selectedChaps.forEach(chapter => {
      const chapterResources = {
        chapter: chapter,
        resources: chapter.related_resources || []
      };

      plan.push(chapterResources);
    });

    return plan;
  }, [selectedChapters]);

  const handleSaveCollection = () => {
    if (!collectionName) return;
    const newCollection = {
      id: Date.now(),
      name: collectionName,
      class: selectedClass,
      chapters: Array.from(selectedChapters),
      date: new Date().toLocaleDateString()
    };
    const updated = [...savedCollections, newCollection];
    setSavedCollections(updated);
    localStorage.setItem('coursePlannerCollections', JSON.stringify(updated));
    setCollectionName('');
    setShowSaveModal(false);
  };

  const loadCollection = (collection) => {
    setSelectedClass(collection.class);
    setSelectedChapters(new Set(collection.chapters));
  };

  const deleteCollection = (id) => {
      const updated = savedCollections.filter(c => c.id !== id);
      setSavedCollections(updated);
      localStorage.setItem('coursePlannerCollections', JSON.stringify(updated));
  }

  const exportData = () => {
    const dataStr = JSON.stringify(generatePlan, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    const exportFileDefaultName = 'course_plan.json';
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  const getIcon = (type) => {
      if (type === 'vSim') return <Activity size={16} className="text-red-500" />;
      if (type.includes('Case Study')) return <FileText size={16} className="text-blue-500" />;
      if (type.includes('CJ Sim')) return <Users size={16} className="text-green-500" />;
      if (type.includes('Notebook')) return <BookOpen size={16} className="text-purple-500" />;
      if (type.includes('CCC')) return <FileDigit size={16} className="text-orange-500" />;
      return <FileText size={16} />;
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col font-sans text-gray-900">
      {/* Header */}
      <header className="bg-indigo-700 text-white p-6 shadow-lg">
        <h1 className="text-4xl font-bold mb-2">Greetings, Queen Randi. What Can I Gather For You Today?</h1>
        <p className="text-indigo-100 text-xl">Automatically aggregate resources for your weekly lessons.</p>
      </header>

      <main className="flex-1 p-6 max-w-7xl mx-auto w-full grid grid-cols-1 md:grid-cols-4 gap-6">
        
        {/* Sidebar: Controls */}
        <aside className="md:col-span-1 bg-white p-6 rounded-xl shadow-md border border-gray-100 h-fit">
          <div className="mb-8">
            <label className="block text-xl font-bold text-gray-800 mb-4">Select Your Class</label>
            <select 
              value={selectedClass} 
              onChange={(e) => { setSelectedClass(e.target.value); setSelectedChapters(new Set()); }}
              className="w-full border-gray-400 border-2 rounded-xl shadow-lg p-4 text-xl bg-white text-gray-900 focus:ring-indigo-600 focus:border-indigo-600 cursor-pointer"
            >
              <option value="">-- Choose Class --</option>
              <option value="Basic Adult Healthcare">Basic Adult Healthcare</option>
              <option value="Pharmacology">Pharmacology</option>
            </select>
          </div>

          {selectedClass && (
            <div className="mb-8">
              <h3 className="text-xl font-bold text-gray-800 mb-4">Select Chapters for Queen Randi</h3>
              <div className="max-h-[500px] overflow-y-auto space-y-2 border border-gray-300 rounded-lg p-3 bg-white shadow-inner custom-scrollbar">
                {chapters.map(ch => (
                  <div 
                    key={ch.id} 
                    className={`flex items-center p-3 rounded-md transition-all duration-200 cursor-pointer ${selectedChapters.has(ch.id) ? 'bg-indigo-100 border border-indigo-200 shadow-sm' : 'hover:bg-gray-50 hover:shadow-sm hover:border-gray-100 border border-transparent'}`}
                    onClick={() => toggleChapter(ch.id)} // Make the whole div clickable
                  >
                    <input
                      type="checkbox"
                      id={`chapter-${ch.id}`} // Unique ID for accessibility
                      checked={selectedChapters.has(ch.id)}
                      onChange={() => {}} // Handle change via div click to avoid double toggle
                      className="mt-1 h-5 w-5 text-indigo-700 focus:ring-indigo-600 border-gray-300 rounded accent-indigo-600 cursor-pointer"
                    />
                    <label htmlFor={`chapter-${ch.id}`} className="ml-3 text-base text-gray-800 font-medium cursor-pointer flex-1">
                      <span className="font-bold text-indigo-800">Ch {ch.number}:</span> {ch.title}
                    </label>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Saved Collections */}
          {savedCollections.length > 0 && (
              <div className="mt-10 pt-6 border-t border-gray-200">
                  <h3 className="text-lg font-semibold text-gray-700 mb-3">Saved Collections</h3>
                  <ul className="space-y-3">
                      {savedCollections.map(col => (
                          <li key={col.id} className="flex justify-between items-center text-base bg-gray-100 p-3 rounded-lg hover:bg-gray-200">
                              <button onClick={() => loadCollection(col)} className="text-left flex-1 truncate font-medium text-indigo-700">
                                  {col.name}
                              </button>
                              <button onClick={() => deleteCollection(col.id)} className="text-red-500 hover:text-red-700 ml-2">
                                  <Trash2 size={14} />
                              </button>
                          </li>
                      ))}
                  </ul>
              </div>
          )}
        </aside>

        {/* Main Content: Results */}
        <section className="md:col-span-3 space-y-6">
          {selectedChapters.size === 0 ? (
            <div className="text-center py-24 bg-white rounded-lg shadow-md border border-dashed border-gray-300">
              <FolderOpen size={64} className="mx-auto text-gray-400 mb-6" />
              <h3 className="text-2xl font-bold text-gray-600 mb-2">No Chapters Selected, Queen Randi!</h3>
              <p className="text-lg text-gray-500">Choose a class and select some chapters to begin gathering your royal resources.</p>
            </div>
          ) : (
            <>
              <div className="flex justify-between items-center bg-white p-5 rounded-lg shadow-md">
                <h2 className="text-2xl font-bold text-gray-800">Your Royal Resource Plan</h2>
                <div className="flex gap-3">
                    <button 
                        onClick={() => setShowSaveModal(true)}
                        className="flex items-center gap-2 px-5 py-2 bg-white border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 text-base font-medium"
                    >
                        <Save size={18} /> Save Collection
                    </button>
                    <button 
                        onClick={exportData}
                        className="flex items-center gap-2 px-5 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 text-base font-medium shadow-sm"
                    >
                        <Download size={18} /> Export List
                    </button>
                </div>
              </div>

              <div className="space-y-8">
                {generatePlan.map((item) => (
                  <div key={item.chapter.id} className="bg-white rounded-lg shadow-lg border border-gray-200 overflow-hidden">
                    <div className="bg-gray-50 px-6 py-4 border-b border-gray-200">
                      <h3 className="text-xl font-bold text-indigo-900">
                        Chapter {item.chapter.number}: {item.chapter.title}
                      </h3>
                    </div>
                    <div className="p-6">
                      {item.resources.length === 0 ? (
                        <p className="text-gray-400 italic text-base">No direct royal resource matches found for this chapter.</p>
                      ) : (
                        <div className="grid grid-cols-1 gap-5">
                          {/* Group by type? Or just list. Grouping looks nicer. */}
                          {['vSim', 'Interactive Case Study', 'CJ Sim', 'The Notebook', 'CCC Page'].map(type => {
                              const typeResources = item.resources.filter(r => 
                                  type === 'vSim' ? r.type === 'vSim' :
                                  type === 'Interactive Case Study' ? r.type === 'Interactive Case Study' :
                                  type === 'CJ Sim' ? r.type === 'CJ Sim' :
                                  type === 'The Notebook' ? r.type === 'The Notebook' :
                                  r.type.includes(type.split(' ')[0]) 
                              );
                              
                              if (typeResources.length === 0) return null;

                              return (
                                  <div key={type} className="mb-4 last:mb-0">
                                      <h4 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3 flex items-center gap-2">
                                          {getIcon(type)} {type}
                                      </h4>
                                      <ul className="space-y-2">
                                          {typeResources.map((res, idx) => (
                                              <li key={idx} className="flex flex-col items-start p-3 bg-gray-50 rounded-lg hover:bg-indigo-50 transition-colors border border-transparent hover:border-indigo-100">
                                                  <span className="text-base font-medium text-gray-800">{res.title}</span>
                                                  {res.description && <span className="text-sm text-gray-600 mt-1">{res.description}</span>}
                                              </li>
                                          ))}
                                      </ul>
                                  </div>
                              );
                          })}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}
        </section>
      </main>

      {/* Save Modal */}
      {showSaveModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-6 z-50">
              <div className="bg-white rounded-lg p-7 max-w-sm w-full shadow-xl">
                  <h3 className="text-xl font-bold mb-5">Save Collection</h3>
                  <input 
                    type="text" 
                    placeholder="Collection Name (e.g., Week 1)" 
                    value={collectionName}
                    onChange={(e) => setCollectionName(e.target.value)}
                    className="w-full border border-gray-300 rounded-lg p-3 mb-5 focus:ring-2 focus:ring-indigo-500 outline-none text-base"
                    autoFocus
                  />
                  <div className="flex justify-end gap-3">
                      <button onClick={() => setShowSaveModal(false)} className="px-5 py-2 text-gray-600 hover:bg-gray-100 rounded-lg text-base">Cancel</button>
                      <button onClick={handleSaveCollection} className="px-5 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 text-base">Save</button>
                  </div>
              </div>
          </div>
      )}
    </div>
  );
};

export default App;
