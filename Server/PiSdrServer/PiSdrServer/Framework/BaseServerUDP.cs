using System;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;

namespace PiSdrServer.Framework
{
    public abstract class BaseServerUDP
    {
        private UdpClient uc;
        
        public BaseServerUDP(int port)
        {
            uc = new UdpClient(port);
            uc.BeginReceive(OnReceivedUdp, null);
        }

        private void OnReceivedUdp(IAsyncResult ar)
        {
            IPEndPoint ep = null;
            byte[] content = uc.EndReceive(ar, ref ep);
            try
            {
                OnDataReceived(content);
            } catch (Exception ex)
            {
                Console.WriteLine($"ERROR IN UDP SERVER: {ex.Message} {ex.StackTrace}");
            }
            uc.BeginReceive(OnReceivedUdp, null);
        }

        public abstract void OnDataReceived(byte[] content);
    }
}
