'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useToast } from '@/hooks/use-toast';
import { runAnalysis } from '@/lib/api';
import { Loader2, PlayCircle } from 'lucide-react';

export default function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();
  const { toast } = useToast();

  const handleRunAnalysis = async () => {
    setIsLoading(true);
    try {
      const result = await runAnalysis();
      localStorage.setItem('analysisResults', JSON.stringify(result));
      router.push('/results');
    } catch (error) {
      toast({
        variant: 'destructive',
        title: 'Analysis Failed',
        description: 'Unable to complete the analysis. Please try again.',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-2xl">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-semibold tracking-tight mb-2">
            EY RFP Analyzer
          </h1>
          <p className="text-muted-foreground">
            Comprehensive proposal analysis and insights
          </p>
        </div>

        <Card className="border-border/50 shadow-xl">
          <CardHeader>
            <CardTitle>Start Analysis</CardTitle>
            <CardDescription>
              Run a comprehensive analysis of your RFP documents to extract technical requirements and pricing information.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="bg-muted/30 rounded-lg p-6 space-y-3">
              <div className="flex items-start gap-3">
                <div className="h-2 w-2 rounded-full bg-primary mt-2" />
                <div>
                  <h3 className="font-medium mb-1">Technical Compliance</h3>
                  <p className="text-sm text-muted-foreground">
                    Evaluate requirements, identify gaps, and assess risk levels
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="h-2 w-2 rounded-full bg-primary mt-2" />
                <div>
                  <h3 className="font-medium mb-1">Pricing Analysis</h3>
                  <p className="text-sm text-muted-foreground">
                    Compare baseline and proposal prices with variance tracking
                  </p>
                </div>
              </div>
            </div>

            <Button
              onClick={handleRunAnalysis}
              disabled={isLoading}
              className="w-full h-12 text-base font-medium"
              size="lg"
            >
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Running Analysis...
                </>
              ) : (
                <>
                  <PlayCircle className="mr-2 h-5 w-5" />
                  Run Analysis
                </>
              )}
            </Button>
          </CardContent>
        </Card>
      </div>
    </main>
  );
}
