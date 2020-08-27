using System;
using System.Collections.Generic;
using System.Net.WebSockets;
using System.Text;
using System.Threading.Tasks;

namespace PiSdrServer.Http.Sockets
{
    public class WaterfallSocket : BaseWebSocket
    {
        public WaterfallSocket() : base(Program.waterfallSocks)
        {
        }

        public override async Task OnReceiveDataBinary(byte[] data, int length)
        {
            
        }

        public override async Task OnReceiveDataText(string text)
        {
            
        }

        public override async Task OnSockClosed(WebSocket socket)
        {
            
        }

        public override async Task OnSockOpened(WebSocket socket)
        {
            
        }
    }
}
