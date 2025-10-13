"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2 } from "lucide-react";

interface AnalysisItem {
  [key: string]: string | number | null;
}

interface AnalysisResult {
  status: string;
  message: string;
  technical_analysis: AnalysisItem[];
  pricing_analysis: AnalysisItem[];
  technical_count: number;
  pricing_count: number;
}

export default function ResultsPage() {
  const [results, setResults] = useState<AnalysisResult>({
    status: "",
    message: "",
    technical_analysis: [],
    pricing_analysis: [],
    technical_count: 0,
    pricing_count: 0,
  });
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchResults = async () => {
      try {
        setIsLoading(true);
        const res = await fetch("http://127.0.0.1:8000/analyze/run", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
        });

        if (!res.ok) throw new Error(`Backend error: ${res.status}`);
        const data = await res.json();
        console.log("✅ Backend Response:", data);

        const formattedResults: AnalysisResult = {
          status: data.status || "unknown",
          message: data.message || "Analysis completed successfully",
          technical_analysis: data.technical || [],
          pricing_analysis: data.pricing || [],
          technical_count: data.technical?.length || 0,
          pricing_count: data.pricing?.length || 0,
        };

        setResults(formattedResults);
      } catch (error) {
        console.error("❌ Error fetching analysis:", error);
        setResults({
          status: "error",
          message: "Failed to fetch results. Please try again.",
          technical_analysis: [],
          pricing_analysis: [],
          technical_count: 0,
          pricing_count: 0,
        });
      } finally {
        setIsLoading(false);
      }
    };

    fetchResults();
  }, []);

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center bg-[#0B0E14] text-gray-100">
        <Loader2 className="animate-spin w-6 h-6 mr-2 text-blue-500" />
        <span className="text-lg">Analyzing tenders...</span>
      </div>
    );
  }

  const renderTable = (data: AnalysisItem[]) => {
    if (!data || data.length === 0) return <p className="text-gray-500">No data available.</p>;

    const keys = Object.keys(data[0]);

    return (
      <div className="overflow-x-auto rounded-lg border border-gray-800 bg-[#0E131F]">
        <table className="min-w-full text-sm text-gray-300">
          <thead className="bg-[#111827] border-b border-gray-700 text-blue-400">
            <tr>
              {keys.map((key) => (
                <th key={key} className="py-2 px-4 text-left capitalize">{key.replace(/_/g, " ")}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, idx) => (
              <tr key={idx} className="border-b border-gray-800 hover:bg-[#141b2c] transition-colors">
                {keys.map((key) => (
                  <td key={key} className="py-2 px-4">
                    {String(row[key] ?? "-")}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  return (
    <div className="p-8 bg-[#0B0E14] min-h-screen text-gray-100">
      <h1 className="text-4xl font-semibold text-blue-400 mb-6">Tender Intelligence Report</h1>

      {/* Technical Analysis */}
      <Card className="bg-[#111827] border border-gray-800 shadow-lg mb-6">
        <CardHeader>
          <CardTitle className="text-blue-300">
            Technical Analysis <span className="text-gray-400 text-sm ml-2">({results.technical_count} Specs)</span>
          </CardTitle>
        </CardHeader>
        <CardContent>{renderTable(results.technical_analysis)}</CardContent>
      </Card>

      {/* Pricing Analysis */}
      <Card className="bg-[#111827] border border-gray-800 shadow-lg mb-6">
        <CardHeader>
          <CardTitle className="text-blue-300">
            Pricing Analysis <span className="text-gray-400 text-sm ml-2">({results.pricing_count} Items)</span>
          </CardTitle>
        </CardHeader>
        <CardContent>{renderTable(results.pricing_analysis)}</CardContent>
      </Card>

      {/* Summary */}
      <Card className="bg-[#111827] border border-gray-800 shadow-lg">
        <CardHeader>
          <CardTitle className="text-blue-300">Summary</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-gray-300">
            <p><span className="font-medium text-gray-400">Status:</span> {results.status}</p>
            <p className="mt-2 text-gray-400">{results.message}</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
