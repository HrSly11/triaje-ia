import React, { useState } from 'react';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import { Download } from 'lucide-react';
import PrintReport from './PrintReport';

const PDFDownload = ({ type, data, selectedDate, selectedMonth, metricas, filename, label = 'Descargar PDF' }) => {
  const [showPreview, setShowPreview] = useState(false);

  const handleDownload = async () => {
    const element = document.getElementById('pdf-print-content');
    if (!element) {
      alert('No se encontró el contenido para exportar');
      return;
    }

    try {
      setShowPreview(false);
      
      await new Promise(resolve => setTimeout(resolve, 100));

      const canvas = await html2canvas(element, {
        scale: 2,
        useCORS: true,
        logging: false,
        backgroundColor: '#ffffff'
      });

      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('p', 'mm', 'a4');
      
      const imgWidth = 210;
      const imgHeight = (canvas.height * imgWidth) / canvas.width;
      
      let heightLeft = imgHeight;
      let position = 0;

      pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
      heightLeft -= pdf.internal.pageSize.height;

      while (heightLeft > 0) {
        position = heightLeft - imgHeight;
        pdf.addPage();
        pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
        heightLeft -= pdf.internal.pageSize.height;
      }

      pdf.save(`${filename}.pdf`);
    } catch (error) {
      console.error('Error al generar PDF:', error);
      alert('Error al generar el PDF. Intente de nuevo.');
    }
  };

  return (
    <>
      <button
        onClick={handleDownload}
        className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium"
      >
        <Download size={18} />
        {label}
      </button>

      <div id="pdf-print-content" style={{ display: 'none', position: 'absolute', left: '-9999px', top: '-9999px' }}>
        <PrintReport 
          type={type}
          data={data}
          selectedDate={selectedDate}
          selectedMonth={selectedMonth}
          metricas={metricas}
        />
      </div>
    </>
  );
};

export default PDFDownload;