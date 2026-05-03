import React, { useState } from 'react';
import DashboardOperativo from './components/DashboardOperativo';
import DashboardGestion from './components/DashboardGestion';
import PDFDownload from './components/PDFDownload';

const App = () => {
  const [activeTab, setActiveTab] = useState('operacional');
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [selectedMonth, setSelectedMonth] = useState(new Date().toISOString().slice(0, 7));

  const formatDateForFilename = (dateStr) => {
    return dateStr.replace(/-/g, '');
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <nav className="bg-white shadow-sm border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xl">T</span>
              </div>
              <div>
                <h1 className="text-lg font-semibold text-slate-800">Triage IA</h1>
                <p className="text-xs text-slate-500">Dashboard de Gestión</p>
              </div>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-slate-800">Panel de Control</h2>
            <p className="text-slate-500">Estadísticas y métricas del sistema de triaje</p>
          </div>
          <div className="flex gap-2">
            {activeTab === 'operacional' ? (
              <PDFDownload 
                targetId="dashboard-operacional" 
                filename={`reporte-operacional-${formatDateForFilename(selectedDate)}`}
                label="Descargar Reporte PDF"
              />
            ) : (
              <PDFDownload 
                targetId="dashboard-gestion" 
                filename={`reporte-gestion-${formatDateForFilename(selectedMonth)}`}
                label="Descargar Reporte PDF"
              />
            )}
          </div>
        </div>

        <div className="flex space-x-1 bg-slate-100 p-1 rounded-lg mb-6 w-fit">
          <button
            onClick={() => setActiveTab('operacional')}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${
              activeTab === 'operacional'
                ? 'bg-white text-primary-600 shadow-sm'
                : 'text-slate-600 hover:text-slate-800'
            }`}
          >
            Operacional
          </button>
          <button
            onClick={() => setActiveTab('gestion')}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${
              activeTab === 'gestion'
                ? 'bg-white text-primary-600 shadow-sm'
                : 'text-slate-600 hover:text-slate-800'
            }`}
          >
            Gestión
          </button>
        </div>

        <div className="mb-6 flex items-center gap-4">
          {activeTab === 'operacional' ? (
            <input
              type="date"
              value={selectedDate}
              onChange={(e) => setSelectedDate(e.target.value)}
              className="px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            />
          ) : (
            <input
              type="month"
              value={selectedMonth}
              onChange={(e) => setSelectedMonth(e.target.value)}
              className="px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            />
          )}
          <span className="text-sm text-slate-500">
            {activeTab === 'operacional' ? 'Seleccionar fecha' : 'Seleccionar mes'}
          </span>
        </div>

        <div id={activeTab === 'operacional' ? 'dashboard-operacional' : 'dashboard-gestion'}>
          {activeTab === 'operacional' ? (
            <DashboardOperativo selectedDate={selectedDate} />
          ) : (
            <DashboardGestion selectedMonth={selectedMonth} />
          )}
        </div>
      </main>

      <footer className="bg-white border-t border-slate-200 mt-8 py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-sm text-slate-500">
          <p>Sistema de Triaje Clínico Asistido por IA - v1.0</p>
          <p className="mt-1">Desarrollado para integración con n8n y HCE</p>
        </div>
      </footer>
    </div>
  );
};

export default App;