using System;
using System.Collections.Generic;
using System.Net.WebSockets;
using System.Text;

namespace PiSdrServer.Http
{
    /// <summary>
    /// Handles distribution of messages to web sockets
    /// </summary>
    public class WebSocketHolder
    {
        private List<BaseWebSocket> socks;

        public WebSocketHolder()
        {
            socks = new List<BaseWebSocket>();
        }

        public void AddSock(BaseWebSocket s)
        {
            lock(socks)
                socks.Add(s);
        }

        public void RemoveSock(BaseWebSocket s)
        {
            lock(socks)
                socks.Remove(s);
        }

        private void DistributeMessage(byte[] buffer, int length, WebSocketMessageType type)
        {
            lock(socks)
            {
                foreach(var s in socks)
                {
#pragma warning disable CS4014 // Because this call is not awaited, execution of the current method continues before the call is completed
                    s.SendData(buffer, length, type);
#pragma warning restore CS4014 // Because this call is not awaited, execution of the current method continues before the call is completed
                }
            }
        }

        public void SendBinary(byte[] content)
        {
            DistributeMessage(content, content.Length, WebSocketMessageType.Binary);
        }
    }
}
