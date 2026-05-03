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

  const total = metricas?.total_triajes || 0;
  const criticos = metricas?.criticos || 0;
  const altos = metricas?.altos || 0;
  const moderados = metricas?.moderados || 0;
  const bajos = metricas?.bajos || 0;
  const pctCriticos = total > 0 ? ((criticos / total) * 100).toFixed(1) : 0;
  const pctAltos = total > 0 ? ((altos / total) * 100).toFixed(1) : 0;
  const pctModerados = total > 0 ? ((moderados / total) * 100).toFixed(1) : 0;
  const pctBajos = total > 0 ? ((bajos / total) * 100).toFixed(1) : 0;

  return (
    <div className="p-8 bg-white" style={{ fontFamily: 'Arial, sans-serif' }}>
      {/* Header */}
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
        <h2 className="text-xl font-semibold text-primary-600 mt-4">
          {type === 'operacional' ? 'REPORTE OPERACIONAL DIARIO' : 'REPORTE DE GESTIÓN MENSUAL'}
        </h2>
        <p className="text-slate-600 mt-1">
          {type === 'operacional' 
            ? `Fecha de Reporte: ${formatDate(selectedDate)}`
            : `Período: ${formatMonth(selectedMonth)}`
          }
        </p>
        <p className="text-sm text-slate-400 mt-1">
          Generado: {new Date().toLocaleString('es-CO')}
        </p>
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
              <div className="flex items-center justify-between">
                <span className="flex items-center gap-2">
                  <span className="w-4 h-4 bg-red-500 rounded"></span>
                  Críticos
                </span>
                <span className="font-semibold">{criticos} ({pctCriticos}%)</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="flex items-center gap-2">
                  <span className="w-4 h-4 bg-orange-500 rounded"></span>
                  Altos
                </span>
                <span className="font-semibold">{altos} ({pctAltos}%)</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="flex items-center gap-2">
                  <span className="w-4 h-4 bg-yellow-500 rounded"></span>
                  Moderados
                </span>
                <span className="font-semibold">{moderados} ({pctModerados}%)</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="flex items-center gap-2">
                  <span className="w-4 h-4 bg-green-500 rounded"></span>
                  Bajos
                </span>
                <span className="font-semibold">{bajos} ({pctBajos}%)</span>
              </div>
            </div>
          </div>
          
          <div>
            <h4 className="font-semibold text-slate-600 mb-2">Indicadores de Rendimiento</h4>
            <div className="space-y-3">
              <div className="p-3 bg-slate-50 rounded">
                <p className="text-sm text-slate-500">Tiempo Promedio de Atención</p>
                <p className="text-xl font-bold text-slate-700">
                  {typeof metricas?.tiempo_promedio_minutos === 'number' 
                    ? `${metricas.tiempo_promedio_minutos.toFixed(1)} minutos` 
                    : 'N/A'}
                </p>
              </div>
              <div className="p-3 bg-slate-50 rounded">
                <p className="text-sm text-slate-500">Tasa de Atención Crítica</p>
                <p className="text-xl font-bold text-red-600">{pctCriticos}%</p>
                {parseFloat(pctCriticos) > 10 && (
                  <p className="text-xs text-red-500 mt-1">⚠ Porcentaje elevado - requiere revisión</p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Detalle por Profesional */}
      {data?.triajes_por_profesional && data.triajes_por_profesional.length > 0 && (
        <div className="mb-6 p-4 bg-white rounded-lg border border-slate-200">
          <h3 className="font-bold text-slate-700 mb-3 border-b border-slate-200 pb-2">DISTRIBUCIÓN POR PROFESIONAL</h3>
          <table className="w-full">
            <thead>
              <tr className="bg-slate-100">
                <th className="text-left p-2 border border-slate-200">Profesional</th>
                <th className="text-center p-2 border border-slate-200">Cantidad</th>
                <th className="text-center p-2 border border-slate-200">Porcentaje</th>
              </tr>
            </thead>
            <tbody>
              {data.triajes_por_profesional.map((item, index) => (
                <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-slate-50'}>
                  <td className="p-2 border border-slate-200">{item.nombre_completo || item.profesional}</td>
                  <td className="text-center p-2 border border-slate-200">{item.cantidad}</td>
                  <td className="text-center p-2 border border-slate-200">
                    {total > 0 ? ((item.cantidad / total) * 100).toFixed(1) : 0}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Detalle por Hora/Día */}
      {type === 'operacional' && data?.triajes_por_hora && data.triajes_por_hora.length > 0 && (
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

      {type === 'gestion' && data?.triajes_por_dia && data.triajes_por_dia.length > 0 && (
        <div className="mb-6 p-4 bg-white rounded-lg border border-slate-200">
          <h3 className="font-bold text-slate-700 mb-3 border-b border-slate-200 pb-2">DISTRIBUCIÓN POR DÍA</h3>
          <table className="w-full">
            <thead>
              <tr className="bg-slate-100">
                <th className="text-left p-2 border border-slate-200">Fecha</th>
                <th className="text-center p-2 border border-slate-200">Cantidad</th>
              </tr>
            </thead>
            <tbody>
              {data.triajes_por_dia.map((item, index) => (
                <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-slate-50'}>
                  <td className="p-2 border border-slate-200">{formatDate(item.fecha)}</td>
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