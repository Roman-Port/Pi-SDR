using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using PiSdrServer.Framework.Servers;
using PiSdrServer.Http;
using PiSdrServer.Http.Sockets;
using System;
using System.Net;
using System.Threading.Tasks;

namespace PiSdrServer
{
    class Program
    {
        public static WebSocketHolder waterfallSocks;

        public static WaterfallServer waterfallServer;
        
        static void Main(string[] args)
        {
            //Create sock holders
            waterfallSocks = new WebSocketHolder();

            //Create servers
            waterfallServer = new WaterfallServer();
            
            //Start
            RunAsync().GetAwaiter().GetResult();
        }

        public static Task RunAsync()
        {
            var host = new WebHostBuilder()
                .UseKestrel(options =>
                {
                    IPAddress addr = IPAddress.Any;
                    options.Listen(addr, ServerStatics.PORT_HTTP);
                })
                .UseStartup<Program>()
                .Configure(Configure)
                .Build();

            return host.RunAsync();
        }

        public static void Configure(IApplicationBuilder app)
        {
            app.UseWebSockets();
            app.Run(OnHTTPRequest);
        }

        public static async Task OnHTTPRequest(HttpContext e)
        {
            //Do CORS stuff
            e.Response.Headers.Add("Access-Control-Allow-Headers", "Authorization");
            e.Response.Headers.Add("Access-Control-Allow-Origin", "*");
            e.Response.Headers.Add("Access-Control-Allow-Methods", "GET, POST, OPTIONS, DELETE, PUT, PATCH");
            if (e.Request.Method.ToUpper() == "OPTIONS")
            {
                return;
            }

            try
            {
                //Find sock to use
                BaseWebSocket sock = null;
                switch (e.Request.Path.ToString())
                {
                    case "/sock/waterfall": sock = new WaterfallSocket(); break;
                }
                if (sock != null)
                {
                    //Run socket
                    await sock.OnRequest(e);
                }
                else
                {
                    //Not found
                    e.Response.StatusCode = 404;
                }
            } catch (Exception ex)
            {
                Console.WriteLine($"ERROR IN HTTP: {ex.Message} {ex.StackTrace}");
            }
        }
    }
}
