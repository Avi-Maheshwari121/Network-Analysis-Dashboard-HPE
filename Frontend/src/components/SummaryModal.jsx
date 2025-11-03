import React from 'react';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

// A simple loading indicator
const LoadingSpinner = () => (
  <div className="text-center p-8">
    <p className="text-primary-accent text-lg">Generating AI Analysis, please wait...</p>
  </div>
);

export default function SummaryModal({ isOpen, isLoading, summaryData, onClose }) {
  // Don't render anything if the modal is closed
  if (!isOpen) return null;

  const handleExportPDF = () => {
    if (!summaryData) return;

    // 1. Initialize the PDF document
    const doc = new jsPDF();
    const primaryColor = [0, 172, 193]; // Your app's primary cyan color
    const lightCyan = [224, 255, 255]; // Light cyan for rows
    const white = [255, 255, 255];
    const black = [0, 0, 0]; 

    // Style "Capture Session Analysis"
    doc.setFontSize(18);
    doc.setFont(undefined, 'bold');
    doc.setTextColor(black[0], black[1], black[2]); 
    doc.text("Capture Session Analysis", 14, 22);
    doc.setFont(undefined, 'normal');

    // Style "Overall Summary"
    doc.setFontSize(14);
    doc.setFont(undefined, 'bold');
    doc.setTextColor(black[0], black[1], black[2]); 
    doc.text("Overall Summary", 14, 32);
    doc.setFont(undefined, 'normal');

    // 3. Add the Summary Paragraph
    doc.setFontSize(11);
    doc.setTextColor(black[0], black[1], black[2]); 
    const summaryLines = doc.splitTextToSize(summaryData.summary, 180);
    doc.text(summaryLines, 14, 38);

    // 4. Calculate table start position
    const tableStartY = 38 + (summaryLines.length * 5) + 5;
    
    // Style "Protocol Breakdown"
    doc.setFontSize(14);
    doc.setFont(undefined, 'bold');
    doc.setTextColor(black[0], black[1], black[2]); 
    doc.text("Protocol Breakdown", 14, tableStartY);
    doc.setFont(undefined, 'normal');

    // 5. Define the table columns and rows
    const tableHead = [['Category', 'Key Metrics', 'Observations']];
    const tableBody = summaryData.breakdown.map(item => [
      item.protocol,
      item.keyMetrics,
      item.observations
    ]);

    // 6. Add the table to the document
    autoTable(doc, {
      head: tableHead,
      body: tableBody,
      startY: tableStartY + 6,
      
      styles: { 
        fontSize: 8, 
        cellPadding: 2, 
        fillColor: white 
      },
      
      alternateRowStyles: { 
        fillColor: lightCyan // Light cyan alternating rows
      },

      headStyles: { 
        fillColor: primaryColor, 
        textColor: white,
        fontStyle: 'bold',
        fontSize : 9
      },
      
      columnStyles: {
        0: { 
          cellWidth: 36, 
          fontStyle: 'bold'
        },
        1: { cellWidth: 73 },  // ~40%
        2: { cellWidth: 73 }   // ~40%
      },

      willDrawCell: (data) => {
        // Check if we are in the 'Key Metrics' column (index 1) and in the body
        if (data.column.index === 1 && data.cell.section === 'body') {
          
          // 1. Get the cell's correct background color
          const cellColor = data.cell.styles.fillColor;
          doc.setFillColor(cellColor[0], cellColor[1], cellColor[2]);
          doc.rect(data.cell.x, data.cell.y, data.cell.width, data.cell.height, 'F');

          // 2. Now draw the custom text
          const lines = data.cell.text;
          doc.setFontSize(data.cell.styles.fontSize);
          
          const lineMetrics = doc.getTextDimensions('M');
          const fontHeight = lineMetrics.h;
          
          const lineHeight = fontHeight * 1.15; 

          let y = data.cell.y + data.cell.padding('top') + fontHeight; 
          const x = data.cell.x + data.cell.padding('left');

          lines.forEach((line) => {
            const parts = line.split(':');
            const key = parts[0] + ':'; 
            const value = parts.slice(1).join(':').trim(); 

            doc.setFont(undefined, 'bold');
            doc.text(key, x, y);

            const keyWidth = doc.getTextWidth(key);
            
            doc.setFont(undefined, 'normal');
            doc.text(value, x + keyWidth + 1, y);
            
            y += lineHeight; 
          });
          
          return false; // Stop autotable from drawing the default text
        }
      }
    });

    // 7. Create a timestamp
    const now = new Date();
    const pad = (num) => String(num).padStart(2, '0');
    
    const dateStr = `${pad(now.getDate())}-${pad(now.getMonth() + 1)}-${now.getFullYear()}`;
    const timeStr = `${pad(now.getHours())}-${pad(now.getMinutes())}-${pad(now.getSeconds())}`;
    const fileName = `network-summary_${dateStr}_${timeStr}.pdf`;

    // 8. Save the PDF with the new filename
    doc.save(fileName);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50 animate-fade-in">
      <div className="bg-surface-dark p-6 rounded-lg shadow-lg w-full max-w-5xl border border-border-dark flex flex-col max-h-[80vh]">
        <div className="flex-shrink-0">
          <h2 className="text-xl font-bold mb-4 text-primary-accent">Capture Session Analysis</h2>
        </div>

        <div className="flex-grow overflow-y-auto pr-2">
          {isLoading ? (
            <LoadingSpinner />
          ) : summaryData ? (
            <>
              {/* Part 1: The Summary Paragraph */}
              <h3 className="font-semibold text-lg mb-2 text-text-primary">Overall Summary</h3>
              <p className="text-text-secondary whitespace-pre-wrap leading-relaxed mb-6">
                {summaryData.summary}
              </p>

              {/* Part 2: The Breakdown Table */}
              <h3 className="font-semibold text-lg mb-3 text-text-primary">Protocol Breakdown</h3>
              <table className="w-full text-left table-auto">
                <thead className="bg-base-dark">
                  <tr>
                    {/* These widths are for the HTML table, they can be % */}
                    <th className="p-2 w-2/12">Protocol</th>
                    <th className="p-2 w-5/12">Key Metrics</th>
                    <th className="p-2 w-5/12">Observations</th>
                  </tr>
                </thead>
                <tbody>
                  {summaryData.breakdown.map((item, index) => (
                    <tr key={index} className="border-t border-border-dark align-top">
                      <td className="p-2 font-bold text-primary-accent">{item.protocol}</td>
                      <td className="p-2 text-text-secondary">
                        {item.keyMetrics.split('\n').map((line, lineIndex) => {
                          const parts = line.split(':');
                          const key = parts[0];
                          const value = parts.slice(1).join(':');
                          return (
                            <div key={lineIndex}>
                              <strong className="text-text-primary">{key}:</strong>
                              <span>{value}</span>
                            </div>
                          );
                        })}
                      </td>
                      <td className="p-2 text-text-secondary">{item.observations}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </>
          ) : (
             <p className="text-text-secondary">No summary data available or an error occurred.</p>
          )}
        </div>

        <div className="flex justify-end mt-6 flex-shrink-0">
          
          {!isLoading && summaryData && summaryData.breakdown.length > 0 && (
            <button
              onClick={handleExportPDF}
              className="bg-primary-accent text-base-dark px-4 py-2 rounded font-bold hover:opacity-90 transition-opacity mr-4"
            >
              Export as PDF
            </button>
          )}

          <button
            onClick={onClose}
            className="bg-primary-accent text-base-dark px-4 py-2 rounded font-bold hover:opacity-90 transition-opacity"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}