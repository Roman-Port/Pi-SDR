using Microsoft.AspNetCore.Http;
using System;
using System.Collections.Generic;
using System.IO;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace PiSdrServer.Http
{
    public abstract class BaseWebSocket
    {
        public abstract Task OnSockOpened(WebSocket socket);
        public abstract Task OnSockClosed(WebSocket socket);
        public abstract Task OnReceiveDataBinary(byte[] data, int length);
        public abstract Task OnReceiveDataText(string text);

        public WebSocket sock;
        public WebSocketHolder holder;

        public BaseWebSocket(WebSocketHolder holder)
        {
            this.holder = holder;
        }

        public async Task OnRequest(HttpContext e)
        {
            if (e.WebSockets.IsWebSocketRequest)
            {
                WebSocket webSocket = await e.WebSockets.AcceptWebSocketAsync();
                await OnAcceptSocket(webSocket);
            }
            else
            {
                e.Response.StatusCode = 400;
            }
        }

        private async Task OnReceiveData(byte[] buffer, int length, WebSocketMessageType type)
        {
            if (type == WebSocketMessageType.Binary)
                await OnReceiveDataBinary(buffer, length);
            else
                await OnReceiveDataText(Encoding.UTF8.GetString(buffer, 0, length));
        }

        private async Task OnAcceptSocket(WebSocket socket)
        {
            //Run the opened function
            this.sock = socket;
            await OnSockOpened(socket);
            holder.AddSock(this);

            try
            {
                //Go into download loop
                byte[] buffer = new byte[16384];
                WebSocketReceiveResult result = await socket.ReceiveAsync(new ArraySegment<byte>(buffer), CancellationToken.None);
                while (!result.CloseStatus.HasValue)
                {
                    if (result.EndOfMessage)
                    {
                        //This is a complete message that fit in a single buffer.
                        await OnReceiveData(buffer, result.Count, result.MessageType);
                    }
                    else
                    {
                        throw new NotImplementedException();
                    }
                    result = await socket.ReceiveAsync(new ArraySegment<byte>(buffer), CancellationToken.None);
                }
                await socket.CloseAsync(result.CloseStatus.Value, result.CloseStatusDescription, CancellationToken.None);
            }
            catch (Exception ex)
            {
                try
                {
                    await sock.CloseAsync(WebSocketCloseStatus.InternalServerError, "INTERNAL_SERVER_ERROR", CancellationToken.None);
                }
                catch { }
                Console.WriteLine($"ERROR IN SOCKET LOOP: " + ex.Message + ex.StackTrace);
            }

            //Send closed message
            holder.RemoveSock(this);
            await OnSockClosed(socket);
        }

        public async Task SendData(string data)
        {
            byte[] buffer = Encoding.UTF8.GetBytes(data);
            await sock.SendAsync(new ArraySegment<byte>(buffer, 0, buffer.Length), WebSocketMessageType.Text, true, CancellationToken.None);
        }

        public async Task SendData(byte[] buffer)
        {
            await sock.SendAsync(new ArraySegment<byte>(buffer, 0, buffer.Length), WebSocketMessageType.Binary, true, CancellationToken.None);
        }

        public async Task SendData(byte[] buffer, int length, WebSocketMessageType type)
        {
            await sock.SendAsync(new ArraySegment<byte>(buffer, 0, length), type, true, CancellationToken.None);
        }

        public async Task DisconnectAsync(WebSocketCloseStatus status, string reason)
        {
            await sock.CloseAsync(status, reason, CancellationToken.None);
        }
    }
}
