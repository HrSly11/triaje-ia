import React from 'react';

const PrintReport = ({ type, data, selectedDate, selectedMonth, metricas }) => {
  const formatDate = (dateStr) => {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return date.toLocaleDateString('es-CO', { 
      day: 'numeric', 
      month: 'long', 
      year: 'numeric' 
    });
  };

  const formatMonth = (monthStr) => {
    if (!monthStr) return '';
    const [year, month] = monthStr.split('-');
    const date = new Date(year, month - 1);
    return date.toLocaleDateString('es-CO', { 
      month: 'long', 
      year: 'numeric' 
    });
  };

  const formatShortDate = (dateStr) => {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return `${date.getDate()} ${date.toLocaleDateString('es-CO', { month: 'short' })}`;
  };

  const total = metricas?.total_triajes || 0;
  const criticos = metricas?.criticos || 0;
  const altos = metricas?.altos || 0;
  const moderados = metricas?.moderados || 0;
  const bajos = metricas?.bajos || 0;
  const pctCriticos = total > 0 ? ((criticos / total) * 100).toFixed(1) : 0;
  const pctAltos = total > 0 ? ((altos / total) * 100).toFixed(1) : 0;
  const pctModerados = total > 0 ? ((moderados / total) * 100).toFixed(1) : 0;
  const pctBajos = total > 0 ? ((bajos / total) * 100).toFixed(1) : 0;

  if (type === 'gestion') {
    return (
      <div className="p-8 bg-slate-50" style={{ fontFamily: 'Segoe UI, Arial, sans-serif' }}>
        {/* Header Gestión - Estilo corporativo */}
        <div className="bg-gradient-to-r from-slate-800 to-slate-700 text-white rounded-xl p-6 mb-6 shadow-lg">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 bg-white/10 rounded-xl flex items-center justify-center backdrop-blur">
                <span className="text-white font-bold text-2xl">T</span>
              </div>
              <div>
                <h1 className="text-xl font-bold">Sistema de Triaje Clínico Asistido por IA</h1>
                <p className="text-slate-300 text-sm">Reporte de Gestión Mensual</p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-slate-400 text-xs">Período</p>
              <p className="text-xl font-bold text-white">{formatMonth(selectedMonth)}</p>
            </div>
          </div>
        </div>

        {/* Resumen Mensual con Grid */}
        <div className="grid grid-cols-4 gap-4 mb-6">
          <div className="bg-white rounded-xl p-5 shadow-sm border-l-4 border-blue-600">
            <p className="text-sm text-slate-500 mb-1">Total del Mes</p>
            <p className="text-4xl font-bold text-slate-800">{total}</p>
            <p className="text-xs text-slate-400 mt-1">{selectedMonth}</p>
          </div>
          <div className="bg-white rounded-xl p-5 shadow-sm border-l-4 border-red-500">
            <p className="text-sm text-slate-500 mb-1">Críticos</p>
            <p className="text-4xl font-bold text-red-600">{criticos}</p>
            <p className="text-xs text-slate-400 mt-1">{pctCriticos}% del total</p>
          </div>
          <div className="bg-white rounded-xl p-5 shadow-sm border-l-4 border-amber-500">
            <p className="text-sm text-slate-500 mb-1">Altos</p>
            <p className="text-4xl font-bold text-amber-600">{altos}</p>
            <p className="text-xs text-slate-400 mt-1">{pctAltos}% del total</p>
          </div>
          <div className="bg-white rounded-xl p-5 shadow-sm border-l-4 border-emerald-500">
            <p className="text-sm text-slate-500 mb-1">Moderados</p>
            <p className="text-4xl font-bold text-emerald-600">{moderados}</p>
            <p className="text-xs text-slate-400 mt-1">{pctModerados}% del total</p>
          </div>
        </div>

        {/* Gráficos y Distribución */}
        <div className="grid grid-cols-2 gap-6 mb-6">
          {/* Triajes por Día - Gráfico de barras visual */}
          {data?.triajes_por_dia && data.triajes_por_dia.length > 0 && (
            <div className="bg-white rounded-xl p-5 shadow-sm">
              <h3 className="font-semibold text-slate-700 mb-4 flex items-center gap-2">
                <span className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center text-blue-600">📅</span>
                Triajes por Día
              </h3>
              <div className="flex items-end justify-between h-40 gap-2 px-2">
                {data.triajes_por_dia.map((item, i) => {
                  const maxVal = Math.max(...data.triajes_por_dia.map(d => d.cantidad), 1);
                  const height = (item.cantidad / maxVal) * 100;
                  return (
                    <div key={i} className="flex flex-col items-center gap-1 flex-1">
                      <div className="w-full bg-blue-200 rounded-t relative" style={{ height: `${height}%`, minHeight: '4px' }}>
                        <div className="absolute -top-5 left-1/2 -translate-x-1/2 text-xs font-semibold text-slate-600">
                          {item.cantidad}
                        </div>
                      </div>
                      <span className="text-xs text-slate-500">{formatShortDate(item.fecha)}</span>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Triajes por Profesional - Gráfico horizontal */}
          {data?.triajes_por_profesional && data.triajes_por_profesional.length > 0 && (
            <div className="bg-white rounded-xl p-5 shadow-sm">
              <h3 className="font-semibold text-slate-700 mb-4 flex items-center gap-2">
                <span className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center text-purple-600">👤</span>
                Triajes por Profesional
              </h3>
              <div className="space-y-3">
                {data.triajes_por_profesional.map((item, i) => {
                  const maxVal = Math.max(...data.triajes_por_profesional.map(p => p.cantidad), 1);
                  const width = (item.cantidad / maxVal) * 100;
                  return (
                    <div key={i} className="flex items-center gap-3">
                      <span className="text-xs text-slate-500 whitespace-nowrap" title={item.nombre_completo || item.profesional}>{item.nombre_completo || item.profesional}</span>
                      <div className="flex-1 h-6 bg-slate-100 rounded-full overflow-hidden">
                        <div className="h-full bg-gradient-to-r from-purple-500 to-purple-400 rounded-full" style={{ width: `${width}%` }}></div>
                      </div>
                      <span className="text-sm font-semibold text-slate-700 w-8 text-right">{item.cantidad}</span>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>

        {/* Distribución por Nivel de Urgencia */}
        {data?.distribucion_urgencia && data.distribucion_urgencia.length > 0 && (
          <div className="bg-white rounded-xl p-5 shadow-sm mb-6">
            <h3 className="font-semibold text-slate-700 mb-4 flex items-center gap-2">
              <span className="w-8 h-8 bg-cyan-100 rounded-lg flex items-center justify-center text-cyan-600">📊</span>
              Distribución por Nivel de Urgencia
            </h3>
            <div className="flex items-center gap-4">
              <div className="flex-1 flex h-4 rounded-full overflow-hidden">
                {data.distribucion_urgencia.map((d, i) => {
                  const colors = { critico: 'bg-red-500', alto: 'bg-amber-500', moderado: 'bg-yellow-400', bajo: 'bg-emerald-500' };
                  return (
                    <div key={i} className={`${colors[d.nivel_urgencia] || 'bg-slate-400'}`} style={{ width: `${(d.cantidad / total) * 100}%` }}></div>
                  );
                })}
              </div>
              <div className="flex gap-4">
                {data.distribucion_urgencia.map((d, i) => {
                  const labels = { critico: 'Críticos', alto: 'Altos', moderado: 'Moderados', bajo: 'Bajos' };
                  return (
                    <span key={i} className="text-xs text-slate-600">
                      <span className="font-semibold">{((d.cantidad / total) * 100).toFixed(0)}%</span> {labels[d.nivel_urgencia]}
                    </span>
                  );
                })}
              </div>
            </div>
          </div>
        )}

        {/* Análisis de Tendencias */}
        <div className="grid grid-cols-3 gap-4">
          <div className="bg-gradient-to-br from-red-50 to-white rounded-xl p-5 border border-red-100">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-slate-500">Casos Críticos</span>
              <span className="text-2xl">⚠️</span>
            </div>
            <p className="text-3xl font-bold text-red-600">{pctCriticos}%</p>
            {parseFloat(pctCriticos) > 20 && (
              <p className="text-xs text-red-500 mt-2 font-medium">⚠ Porcentaje elevado - revisar procesos</p>
            )}
          </div>
          <div className="bg-gradient-to-br from-amber-50 to-white rounded-xl p-5 border border-amber-100">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-slate-500">Casos de Alta Prioridad</span>
              <span className="text-2xl">🔶</span>
            </div>
            <p className="text-3xl font-bold text-amber-600">{pctAltos}%</p>
          </div>
          <div className="bg-gradient-to-br from-blue-50 to-white rounded-xl p-5 border border-blue-100">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-slate-500">Promedio de Tiempo</span>
              <span className="text-2xl">⏱️</span>
            </div>
            <p className="text-3xl font-bold text-blue-600">
              {metricas?.tiempo_promedio_minutos != null 
                ? `${parseFloat(metricas.tiempo_promedio_minutos).toFixed(0)} min` 
                : 'N/A'}
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-8 pt-4 border-t border-slate-200 text-center">
          <p className="text-slate-500 text-sm">
            Sistema de Triaje Clínico Asistido por IA | Generado: {new Date().toLocaleString('es-CO')}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8 bg-white" style={{ fontFamily: 'Arial, sans-serif' }}>
      {/* Header Operacional - Estilo simple */}
      <div className="text-center border-b-2 border-slate-300 pb-4 mb-6">
        <div className="flex items-center justify-center gap-4 mb-2">
          <div className="w-16 h-16 bg-primary-600 rounded-xl flex items-center justify-center">
            <span className="text-white font-bold text-3xl">T</span>
          </div>
          <div>
            <h1 className="text-2xl font-bold text-slate-800">Sistema de Triaje Clínico Asistido por IA</h1>
            <p className="text-slate-500">Hospital de Alta Complejidad - Gestión de Urgencias</p>
          </div>
        </div>
        <h2 className="text-xl font-semibold text-primary-600 mt-4">REPORTE OPERACIONAL DIARIO</h2>
        <p className="text-slate-600 mt-1">Fecha de Reporte: {formatDate(selectedDate)}</p>
        <p className="text-sm text-slate-400 mt-1">Generado: {new Date().toLocaleString('es-CO')}</p>
      </div>

      {/* Resumen Ejecutivo */}
      <div className="mb-6 p-4 bg-slate-50 rounded-lg border border-slate-200">
        <h3 className="font-bold text-slate-700 mb-3 border-b border-slate-200 pb-2">RESUMEN EJECUTIVO</h3>
        <div className="grid grid-cols-5 gap-4 text-center">
          <div className="p-3 bg-white rounded-lg border border-slate-200">
            <p className="text-3xl font-bold text-slate-800">{total}</p>
            <p className="text-sm text-slate-500">Total Triajes</p>
          </div>
          <div className="p-3 bg-red-50 rounded-lg border border-red-200">
            <p className="text-3xl font-bold text-red-600">{criticos}</p>
            <p className="text-sm text-slate-500">Críticos ({pctCriticos}%)</p>
          </div>
          <div className="p-3 bg-orange-50 rounded-lg border border-orange-200">
            <p className="text-3xl font-bold text-orange-600">{altos}</p>
            <p className="text-sm text-slate-500">Altos ({pctAltos}%)</p>
          </div>
          <div className="p-3 bg-yellow-50 rounded-lg border border-yellow-200">
            <p className="text-3xl font-bold text-yellow-600">{moderados}</p>
            <p className="text-sm text-slate-500">Moderados ({pctModerados}%)</p>
          </div>
          <div className="p-3 bg-green-50 rounded-lg border border-green-200">
            <p className="text-3xl font-bold text-green-600">{bajos}</p>
            <p className="text-sm text-slate-500">Bajos ({pctBajos}%)</p>
          </div>
        </div>
      </div>

      {/* Análisis */}
      <div className="mb-6 p-4 bg-white rounded-lg border border-slate-200">
        <h3 className="font-bold text-slate-700 mb-3 border-b border-slate-200 pb-2">ANÁLISIS DE INDICADORES</h3>
        <div className="grid grid-cols-2 gap-6">
          <div>
            <h4 className="font-semibold text-slate-600 mb-2">Clasificación por Nivel de Urgencia</h4>
            <div className="space-y-2">
              {[['Críticos', criticos, pctCriticos, 'bg-red-500'], ['Altos', altos, pctAltos, 'bg-orange-500'], ['Moderados', moderados, pctModerados, 'bg-yellow-500'], ['Bajos', bajos, pctBajos, 'bg-green-500']].map(([label, val, pct, color]) => (
                <div key={label} className="flex items-center justify-between">
                  <span className="flex items-center gap-2">
                    <span className={`w-4 h-4 ${color} rounded`}></span>
                    {label}
                  </span>
                  <span className="font-semibold">{val} ({pct}%)</span>
                </div>
              ))}
            </div>
          </div>
          <div>
            <h4 className="font-semibold text-slate-600 mb-2">Indicadores de Rendimiento</h4>
            <div className="space-y-3">
              <div className="p-3 bg-slate-50 rounded">
                <p className="text-sm text-slate-500">Tiempo Promedio de Atención</p>
                <p className="text-xl font-bold text-slate-700">
                  {metricas?.tiempo_promedio_minutos != null ? `${parseFloat(metricas.tiempo_promedio_minutos).toFixed(1)} minutos` : 'N/A'}
                </p>
              </div>
              <div className="p-3 bg-slate-50 rounded">
                <p className="text-sm text-slate-500">Tasa de Atención Crítica</p>
                <p className="text-xl font-bold text-red-600">{pctCriticos}%</p>
                {parseFloat(pctCriticos) > 10 && <p className="text-xs text-red-500 mt-1">⚠ Porcentaje elevado - requiere revisión</p>}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Distribución por Hora */}
      {data?.triajes_por_hora && data.triajes_por_hora.length > 0 && (
        <div className="mb-6 p-4 bg-white rounded-lg border border-slate-200">
          <h3 className="font-bold text-slate-700 mb-3 border-b border-slate-200 pb-2">DISTRIBUCIÓN POR HORA</h3>
          <table className="w-full">
            <thead>
              <tr className="bg-slate-100">
                <th className="text-left p-2 border border-slate-200">Hora</th>
                <th className="text-center p-2 border border-slate-200">Cantidad</th>
              </tr>
            </thead>
            <tbody>
              {data.triajes_por_hora.map((item, index) => (
                <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-slate-50'}>
                  <td className="p-2 border border-slate-200">{item.nombre || item.hora}</td>
                  <td className="text-center p-2 border border-slate-200">{item.cantidad}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Footer */}
      <div className="mt-8 pt-4 border-t-2 border-slate-300 text-center text-sm text-slate-500">
        <p className="font-semibold">Sistema de Triaje Clínico Asistido por IA - v1.0</p>
        <p className="mt-1">Integración con n8n Workflow Automation y HCE</p>
        <p className="mt-1 text-slate-400">Este documento es generado automáticamente y no requiere firma.</p>
      </div>
    </div>
  );
};

export default PrintReport;