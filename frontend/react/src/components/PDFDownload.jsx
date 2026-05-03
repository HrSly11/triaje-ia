import React from 'react';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import { Download } from 'lucide-react';
import PrintReport from './PrintReport';

const PDFDownload = ({ type, data, selectedDate, selectedMonth, metricas, filename, label = 'Descargar PDF' }) => {
  const handleDownload = async () => {
    const container = document.createElement('div');
    container.id = 'pdf-temp-container';
    container.style.cssText = `
      position: fixed;
      left: -9999px;
      top: 0;
      width: 1200px;
      background: white;
      z-index: -1;
    `;
    
    const printContent = document.createElement('div');
    printContent.innerHTML = document.getElementById('pdf-print-content').innerHTML;
    container.appendChild(printContent);
    document.body.appendChild(container);
    
    try {
      await new Promise(resolve => setTimeout(resolve, 500));

      const canvas = await html2canvas(container, {
        scale: 2,
        useCORS: true,
        logging: false,
        backgroundColor: '#ffffff',
        allowTaint: true
      });

      const imgData = canvas.toDataURL('image/jpeg', 0.95);
      const pdf = new jsPDF('p', 'mm', 'a4');
      
      const imgWidth = 210;
      const pageHeight = 297;
      const imgHeight = (canvas.height * imgWidth) / canvas.width;
      
      let heightLeft = imgHeight;
      let position = 0;

      pdf.addImage(imgData, 'JPEG', 0, position, imgWidth, imgHeight);
      heightLeft -= pageHeight;

      while (heightLeft > 0) {
        position = heightLeft - imgHeight;
        pdf.addPage();
        pdf.addImage(imgData, 'JPEG', 0, position, imgWidth, imgHeight);
        heightLeft -= pageHeight;
      }

      pdf.save(`${filename}.pdf`);
    } catch (error) {
      console.error('Error al generar PDF:', error);
      alert('Error al generar el PDF. Intente de nuevo.');
    } finally {
      if (container.parentNode) {
        container.parentNode.removeChild(container);
      }
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

      <div id="pdf-print-content" style={{ display: 'none' }}>
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