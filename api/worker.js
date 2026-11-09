/**
 * Pixel2Vector AI Studio - Serverless API & Edge Worker
 * Author: Pickko | Organization: PixelPie Media
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // Health probe
    if (url.pathname === '/api/health') {
      return new Response(JSON.stringify({
        status: 'UP',
        service: 'Pixel2Vector AI Studio',
        author: 'Pickko',
        version: '1.0.0',
        timestamp: new Date().toISOString()
      }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    // Vectorize endpoint (raster to vector or DOM to vector)
    if (url.pathname === '/api/vectorize' && request.method === 'POST') {
      try {
        const body = await request.json();
        const { target, format = 'svg', colors = 16, deepBezier = true } = body;

        if (!target) {
          return new Response(JSON.stringify({ error: 'Target image or URL is required' }), {
            status: 400,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
          });
        }

        // Mock conversion response with mathematical cubic bezier geometry
        const responseData = {
          success: true,
          target: target,
          format: format,
          colorCount: colors,
          bezierOptimization: deepBezier,
          vectorData: {
            pathsCount: 42,
            viewBox: '0 0 800 600',
            svgSnippet: '<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 800 600\"><path d=\"M50 150 C100 80, 200 80, 250 150 S350 220, 400 150\" fill=\"none\" stroke=\"#06B6D4\" stroke-width=\"4\"/></svg>'
          },
          generatedAt: new Date().toISOString()
        };

        return new Response(JSON.stringify(responseData), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      } catch (err) {
        return new Response(JSON.stringify({ error: err.message }), {
          status: 500,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }
    }

    // Stripe checkout session creation
    if (url.pathname === '/api/checkout' && request.method === 'POST') {
      const body = await request.json().catch(() => ({}));
      const plan = body.plan || 'pro_monthly';

      return new Response(JSON.stringify({
        session_id: 'cs_test_' + Math.random().toString(36).substring(2, 15),
        checkout_url: 'https://checkout.stripe.com/c/pay/test_session',
        plan: plan,
        currency: 'usd',
        amount: plan === 'lifetime' ? 9900 : 2900,
        status: 'READY'
      }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    return new Response(JSON.stringify({ error: 'Not Found' }), {
      status: 404,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }
};
