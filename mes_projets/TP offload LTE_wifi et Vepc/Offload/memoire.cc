/* -*-  Mode: C++; c-file-style: "gnu"; indent-tabs-mode:nil; -*- */



#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/mobility-module.h"
#include "ns3/lte-module.h"
#include "ns3/config-store.h"
#include <ns3/buildings-helper.h>
//#include "ns3/gtk-config-store.h"
#include <stdint.h>
#include <string>
#include "ns3/object-factory.h"
#include "ns3/address.h"
#include "ns3/attribute.h"
#include "ns3/net-device.h"
#include "ns3/node-container.h"
#include "ns3/application-container.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/csma-module.h"
#include "ns3/internet-module.h"
#include "ns3/yans-wifi-helper.h"
#include "ns3/ssid.h"
#include "ns3/flow-monitor-helper.h"
 #include "ns3/flow-monitor.h"
 #include "ns3/ipv4-flow-classifier.h"
 #include "ns3/ipv4-flow-probe.h"
 #include "ns3/ipv4-l3-protocol.h"
 #include "ns3/ipv6-flow-classifier.h"
 #include "ns3/ipv6-flow-probe.h"
 #include "ns3/ipv6-l3-protocol.h"
 #include "ns3/node.h"
 #include "ns3/node-list.h"
 #include "ns3/nstime.h"
 #include "ns3/ipv4-global-routing-helper.h"
 #include "ns3/simulator.h"
 #include "ns3/netanim-module.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("Offloading");
double debit;
double deb[5];
double info_lte[10][3];
double info_wifi[10][1];
uint32_t resourceId[5];
uint8_t protocole;
uint8_t protocol[5];
double simtime=10.0;
ApplicationContainer onOffApp_lte;
ApplicationContainer sinkApps_lte;
ApplicationContainer onOffApp_lte1;
ApplicationContainer sinkApps_lte1;
ApplicationContainer onOffApp_lte2;
ApplicationContainer sinkApps_lte2;
ApplicationContainer sinkApps_lte_offload;
ApplicationContainer onOffApp_lte_offload;
Time now;
int numero_appli_udp=0;
int numero_flux[5];
int numero_appli_tcp=0;
int numero_appli_tcp_wifi=0;
int numero_appli_udp_wifi=0;

void remise_a_zero()
{
        int i=0;
         for(i=0;i<5;i++)
         {
                numero_flux[i]=0;
                protocol[i]=0;
                deb[i]=0.00000;
         }                           
}
void appli1(ApplicationContainer serveur, ApplicationContainer receveur,Ptr<Node> server,Ptr<Node>client,Ipv4Address address)
{
        uint16_t dlPort = 1234;
        
        Ptr<UniformRandomVariable> y = CreateObject<UniformRandomVariable> ();
        y->SetAttribute ("Min", DoubleValue (0.0));
        y->SetAttribute ("Max", DoubleValue (1.0));
        if (protocole == 17)
        {
        PacketSinkHelper packetSinkHelper_lte ("ns3::UdpSocketFactory", InetSocketAddress (Ipv4Address::GetAny (), dlPort));
        receveur.Add(packetSinkHelper_lte.Install(client));
       
      
        OnOffHelper VoIPonOffHelper_lte("ns3::UdpSocketFactory", InetSocketAddress(address, dlPort)); //OnOffApplication, UDP traffic, Please refer the ns-3 API;   
        VoIPonOffHelper_lte.SetAttribute("OnTime", StringValue ("ns3::ConstantRandomVariable[Constant=1]"));
        VoIPonOffHelper_lte.SetAttribute("OffTime", StringValue ("ns3::ConstantRandomVariable[Constant=0]"));
        VoIPonOffHelper_lte.SetAttribute("DataRate", DataRateValue(DataRate("10Mbps"))); //Traffic Bit Rate
        VoIPonOffHelper_lte.SetAttribute("PacketSize", UintegerValue(1472));
        //VoIPonOffHelper_lte.SetAttribute("StartTime", TimeValue(Seconds(y->GetValue ())));
        serveur.Add(VoIPonOffHelper_lte.Install(server));
        receveur.Start(Seconds (0.0));
        serveur.Start(Seconds (y->GetValue ()));
        serveur.Stop(Seconds(2.0));
        receveur.Stop(Seconds(2.0));
        }
        if (protocole == 6)
        {
        PacketSinkHelper packetSinkHelper_lte ("ns3::TcpSocketFactory", InetSocketAddress (Ipv4Address::GetAny (), dlPort));
        receveur.Add(packetSinkHelper_lte.Install(client));
      
        OnOffHelper VoIPonOffHelper_lte("ns3::TcpSocketFactory", InetSocketAddress(address, dlPort)); //OnOffApplication, UDP traffic, Please refer the ns-3 API;      
        VoIPonOffHelper_lte.SetAttribute("OnTime", StringValue ("ns3::ConstantRandomVariable[Constant=1]"));
        VoIPonOffHelper_lte.SetAttribute("OffTime", StringValue ("ns3::ConstantRandomVariable[Constant=0]"));
        VoIPonOffHelper_lte.SetAttribute("DataRate", DataRateValue(DataRate("10Mbps"))); //Traffic Bit Rate
        VoIPonOffHelper_lte.SetAttribute("PacketSize", UintegerValue(1472));
        //VoIPonOffHelper_lte.SetAttribute("StartTime", TimeValue(Seconds(y->GetValue ())));
        serveur.Add(VoIPonOffHelper_lte.Install(server));
        receveur.Start(Seconds (0.0));
        serveur.Start(Seconds (y->GetValue ()));
        }
}

void appli2(ApplicationContainer serveur, ApplicationContainer receveur,Ptr<Node> server,Ptr<Node>client,Ipv4Address address)
{
        uint16_t dlPort = 1235;
        
        Ptr<UniformRandomVariable> y = CreateObject<UniformRandomVariable> ();
        y->SetAttribute ("Min", DoubleValue (0.0));
        y->SetAttribute ("Max", DoubleValue (1.0));
        if (protocole == 17)
        {
        PacketSinkHelper packetSinkHelper_lte1 ("ns3::UdpSocketFactory", InetSocketAddress (Ipv4Address::GetAny (), dlPort));
        receveur.Add(packetSinkHelper_lte1.Install(client));
      
        OnOffHelper VoIPonOffHelper_lte1("ns3::UdpSocketFactory", InetSocketAddress(address, dlPort)); //OnOffApplication, UDP traffic, Please refer the ns-3 API;      
        VoIPonOffHelper_lte1.SetAttribute("OnTime", StringValue ("ns3::ConstantRandomVariable[Constant=1]"));
        VoIPonOffHelper_lte1.SetAttribute("OffTime", StringValue ("ns3::ConstantRandomVariable[Constant=0]"));
        VoIPonOffHelper_lte1.SetAttribute("DataRate", DataRateValue(DataRate("50Mbps"))); //Traffic Bit Rate
        VoIPonOffHelper_lte1.SetAttribute("PacketSize", UintegerValue(1472));
        //VoIPonOffHelper_lte.SetAttribute("StartTime", TimeValue(Seconds(y->GetValue ())));
        serveur.Add(VoIPonOffHelper_lte1.Install(server));
        receveur.Start(Seconds (0.0));
        serveur.Start(Seconds (y->GetValue ()));
        }
        if (protocole == 6)
        {
        PacketSinkHelper packetSinkHelper_lte1 ("ns3::TcpSocketFactory", InetSocketAddress (Ipv4Address::GetAny (), dlPort));
        receveur.Add(packetSinkHelper_lte1.Install(client));
      
        OnOffHelper VoIPonOffHelper_lte1("ns3::TcpSocketFactory", InetSocketAddress(address, dlPort)); //OnOffApplication, UDP traffic, Please refer the ns-3 API;      
        VoIPonOffHelper_lte1.SetAttribute("OnTime", StringValue ("ns3::ConstantRandomVariable[Constant=1]"));
        VoIPonOffHelper_lte1.SetAttribute("OffTime", StringValue ("ns3::ConstantRandomVariable[Constant=0]"));
        VoIPonOffHelper_lte1.SetAttribute("DataRate", DataRateValue(DataRate("50Mbps"))); //Traffic Bit Rate
        VoIPonOffHelper_lte1.SetAttribute("PacketSize", UintegerValue(1472));
        //VoIPonOffHelper_lte.SetAttribute("StartTime", TimeValue(Seconds(y->GetValue ())));
        serveur.Add(VoIPonOffHelper_lte1.Install(server));
        receveur.Start(Seconds (0.0));
        serveur.Start(Seconds (y->GetValue ()));
        }
}

void appli3(ApplicationContainer serveur, ApplicationContainer receveur,Ptr<Node> server,Ptr<Node>client,Ipv4Address address)
{
        uint16_t dlPort = 1236;
        Ptr<UniformRandomVariable> y = CreateObject<UniformRandomVariable> ();
        y->SetAttribute ("Min", DoubleValue (0.0));
        y->SetAttribute ("Max", DoubleValue (1.0));

        PacketSinkHelper packetSinkHelper_lte2 ("ns3::UdpSocketFactory", InetSocketAddress (Ipv4Address::GetAny (), dlPort));
        receveur.Add(packetSinkHelper_lte2.Install(client));
      
        OnOffHelper VoIPonOffHelper_lte2("ns3::UdpSocketFactory", InetSocketAddress(address, dlPort)); //OnOffApplication, UDP traffic, Please refer the ns-3 API;      
        VoIPonOffHelper_lte2.SetAttribute("OnTime", StringValue ("ns3::ConstantRandomVariable[Constant=1]"));
        VoIPonOffHelper_lte2.SetAttribute("OffTime", StringValue ("ns3::ConstantRandomVariable[Constant=0]"));
        VoIPonOffHelper_lte2.SetAttribute("DataRate", DataRateValue(DataRate("64Kbps"))); //Traffic Bit Rate
        VoIPonOffHelper_lte2.SetAttribute("PacketSize", UintegerValue(60));
        //VoIPonOffHelper_lte.SetAttribute("StartTime", TimeValue(Seconds(y->GetValue ())));
        serveur.Add(VoIPonOffHelper_lte2.Install(server));
        receveur.Start(Seconds (0.0));
        serveur.Start(Seconds (y->GetValue ()));
}

void affichage_info(std::map<FlowId,FlowMonitor::FlowStats>::const_iterator i,Ipv4FlowClassifier::FiveTuple t)
{
       std::cout<<"\n Flux "<<i->first <<"("<<t.sourceAddress<<"-> "<<t.destinationAddress<<")\n";
       std::cout<<"Tx Bytes "<<i->second.txBytes<<"\n";
       std::cout<<"Rx Bytes "<<i->second.txBytes<<"\n"; 
}

void affichage_debit_protocole_numero(double debit,uint8_t protocole,std::map<FlowId,FlowMonitor::FlowStats>::const_iterator i,int numero_appli,bool uplink,bool wifi)
{
        if(wifi==false)
        {
                if(uplink==false)
                {
                        if(protocole==17)
                        {
                                std::cout<<"le numéro de l'appli en dl Udp en Lte est : "<<numero_appli<<"\n";
                                std::cout<<"protocole de couche 4 utilisé est : Udp \n";
                        }
                        if(protocole==6)
                        {
                                std::cout<<"le numéro de l'appli en dl Tcp en Lte est : "<<numero_appli_tcp<<" \n";
                                std::cout<<"protocole de couche 4 utilisé est : Tcp \n";
                        }
                        std::cout<<"le debit de l'application "<<i->first<<" en lte est: "<<debit<< " Mbps\n";
                }
                else
                {
                        if(protocole==17)
                        {
                                std::cout<<"le numéro de l'appli en ul Udp en Lte est : "<<numero_appli<<"\n";
                                std::cout<<"protocole de couche 4 utilisé est : Udp \n";
                        }
                        if(protocole==6)
                        {
                                std::cout<<"le numéro de l'appli en ul Tcp en Lte est : "<<numero_appli_tcp<<" \n";
                                std::cout<<"protocole de couche 4 utilisé est : Tcp \n";
                        }
                         std::cout<<"le debit de l'application en ul lte "<<i->first-1<<" en lte est: "<<debit<< " Mbps\n";
                }
        }
        else
        {
                if(uplink==false)
                {
                        if(protocole==17)
                        {
                                std::cout<<"le numéro de l'appli en dl Udp en wifi est : "<<numero_appli<<"\n";
                                std::cout<<"protocole de couche 4 utilisé est : Udp \n";
                        }
                        if(protocole==6)
                        {
                                std::cout<<"le numéro de l'appli en dl Tcp en wifi est : "<<numero_appli_tcp<<" \n";
                                std::cout<<"protocole de couche 4 utilisé est : Tcp \n";
                        }
                        std::cout<<"le debit de l'application "<<i->first<<" en wifi est: "<<debit<< " Mbps\n";
                }
                else
                {
                        if(protocole==17)
                        {
                                std::cout<<"le numéro de l'appli en ul Udp en wifi est : "<<numero_appli<<"\n";
                                std::cout<<"protocole de couche 4 utilisé est : Udp \n";
                        }
                        if(protocole==6)
                        {
                                std::cout<<"le numéro de l'appli en ul Tcp en wifi est : "<<numero_appli_tcp<<" \n";
                                std::cout<<"protocole de couche 4 utilisé est : Tcp \n";
                        }
                        std::cout<<"le debit de l'application en ul wifi "<<i->first-1<<" en lte est: "<<debit<< " Mbps\n";
                }
        }       
}
void throughputMonitor(FlowMonitorHelper *fmHelper, Ptr<FlowMonitor> flowMon)
{       
        now=Simulator::Now();
        int seconde=int(now.GetSeconds());
        std::cout<<" \n le temps de simulation est :"<<now.GetSeconds()<<" Secondes\n";
        flowMon->CheckForLostPackets();
        Ptr<Ipv4FlowClassifier> classifier= DynamicCast<Ipv4FlowClassifier> (fmHelper->GetClassifier());
        std::map<FlowId,FlowMonitor::FlowStats> stats=flowMon->GetFlowStats();
        std::map<FlowId,FlowMonitor::FlowStats>::const_iterator i;
        numero_appli_udp=0;
        numero_appli_tcp=0;
        numero_appli_tcp_wifi=0;
        numero_appli_udp_wifi=0;
        int j=0,k=0;
        for(std::map<FlowId,FlowMonitor::FlowStats>::const_iterator i=stats.begin();i!=stats.end();++i)
        {
              
                Ipv4FlowClassifier::FiveTuple t =classifier->FindFlow(i->first);
                if(Ipv4Address("7.0.0.0") < t.destinationAddress &&  t.destinationAddress < Ipv4Address("7.0.0.255"))
                {
                        protocole=t.protocol;
                        protocol[j]=protocole;
                        numero_flux[i->first]=i->first;
                        NS_LOG_DEBUG("Flux "<<i->first <<"("<<t.sourceAddress<<"-> "<<t.destinationAddress<<")");
                        affichage_info(i,t);
                        debit=(i->second.txBytes*8.0)/((i->second.timeLastRxPacket.GetSeconds()-i->second.timeFirstTxPacket.GetSeconds())*1024*1024);
                        deb[j]=debit;
                        info_lte[seconde][k]=debit;
                        j=j+1;
                        k=k+1;
                        if (protocole==17)
                        {
                                numero_appli_udp=numero_appli_udp+1;
                                affichage_debit_protocole_numero(debit,protocole,i, numero_appli_udp,false,false);
                        }
                        if(protocole ==6)
                        {
                                numero_appli_tcp=numero_appli_tcp+1;
                                affichage_debit_protocole_numero(debit,protocole,i, numero_appli_tcp,false,false);
                                if(debit>1.0)
                                { 
                                        std::cout<<"l'application est toujours transporté par le réseau Lte \n";        
                                }
                        }
                }
                if(Ipv4Address("10.0.0.0")< t.destinationAddress &&  t.destinationAddress < Ipv4Address("10.0.0.3"))
                {
                        protocole=t.protocol;
                        protocol[j]=protocole;
                        numero_flux[i->first-1]=i->first;
                        affichage_info(i,t);
                        debit=(i->second.txBytes*8.0)/((i->second.timeLastRxPacket.GetSeconds()-i->second.timeFirstTxPacket.GetSeconds())*1024*1024);
                        if (protocole==17)
                        {
                                affichage_debit_protocole_numero(debit,protocole,i, numero_appli_udp,true,false);
                        }
                        if(protocole ==6)
                        {
                                affichage_debit_protocole_numero(debit,protocole,i, numero_appli_tcp,true,false);
                        }
                
                }
                if(Ipv4Address("10.1.0.0")< t.destinationAddress &&  t.destinationAddress < Ipv4Address("10.1.0.255"))
                {
                        affichage_info(i,t);
                        debit=(i->second.txBytes*8.0)/((i->second.timeLastRxPacket.GetSeconds()-i->second.timeFirstTxPacket.GetSeconds())*1024*1024);
                        info_wifi[seconde][1]=debit;
                        protocole=t.protocol;
                       if (protocole==17)
                        {
                                numero_appli_udp_wifi= numero_appli_udp_wifi+1;
                                affichage_debit_protocole_numero(debit,protocole,i, numero_appli_udp_wifi,false,true);
                        }
                        if(protocole ==6)
                        {
                                numero_appli_udp_wifi= numero_appli_tcp_wifi+1;
                                affichage_debit_protocole_numero(debit,protocole,i, numero_appli_tcp_wifi,false,true);                                
                        }
                
                }    
        }
        std::cout<<"\n";
        Simulator::Schedule(Seconds(1),&throughputMonitor,fmHelper,flowMon);
}

void recapitulatif_lte(double info_l[][3],double info_w[][1],int tps,int nbre_appli_lte,int nbre_appli_wifi)
{
        std::cout<<"\nRECAPITULATIF DES DEBITS EN LTE ET WIFI\n\n";
        std::cout<<"secondes\t";
        int i=0,j=0;
        for (i=1;i<=nbre_appli_lte;i++)
        {
                std::cout<<"debit_appli_lte["<<i<<"] en Mbps\t";
        }
        i=1;
        std::cout<<"debit_appli_wifi["<<i<<"] en Mbps\t";
        std::cout<<"\n";
        i=0;
        for(i=0;i<=tps;i++)
        {
                std::cout<<i<<"s\t\t";
                for(j=0;j<nbre_appli_lte;j++)
                {
                        std::cout<<info_l[i][j]<<"\t\t\t\t";
                }
                for(j=0;j<nbre_appli_wifi;j++)
                {
                        std::cout<<info_w[i+1][j]<<"\t";
                }
                std::cout<<"\n";
        }
}


void offload(uint8_t proto[],double debt[],Ptr<Node> server,Ptr<Node>client,Ipv4Address address)
{
        int i=0;
        for(i=0;i<3;i++)
        {       
                if(proto[i]==17 && debt[i]>1.0)
                {
                        now=Simulator::Now();
                        std::cout<<"\n Arrêt appli "<<i+1<<" à la seconde: "<<now.GetSeconds()<<" \n";
                        onOffApp_lte.Stop(Seconds(now.GetSeconds()));
                        sinkApps_lte.Stop(Seconds(now.GetSeconds()));
                        int dlPort_off = 8765;
                        PacketSinkHelper packetSinkHelper_lte_offload ("ns3::UdpSocketFactory", InetSocketAddress (Ipv4Address::GetAny (), dlPort_off));
                        sinkApps_lte_offload.Add(packetSinkHelper_lte_offload.Install(client));
        
                        OnOffHelper VoIPonOffHelper_lte_offload("ns3::UdpSocketFactory", InetSocketAddress(address, dlPort_off));   
                        VoIPonOffHelper_lte_offload.SetAttribute("OnTime", StringValue ("ns3::ConstantRandomVariable[Constant=1]"));
                        VoIPonOffHelper_lte_offload.SetAttribute("OffTime", StringValue ("ns3::ConstantRandomVariable[Constant=0]"));
                        VoIPonOffHelper_lte_offload.SetAttribute("DataRate", DataRateValue(DataRate("10Mbps"))); //Traffic Bit Rate
                        VoIPonOffHelper_lte_offload.SetAttribute("PacketSize", UintegerValue(1472));
                        onOffApp_lte.Add(VoIPonOffHelper_lte_offload.Install(server));
                        sinkApps_lte_offload.Start(now);
                        onOffApp_lte_offload.Start(now);
                        
                }
        }                      
}

int main (int argc, char *argv[])
{	
    //Lte implementation
       
	//double Avgthroughput_lte = 0.0;
        double simTime = 300.0;
        Ptr<PacketSink> sink; 
        LogComponentEnable ("LteHelper", LOG_LEVEL_INFO);
        LogComponentEnable ("LteEnbNetDevice",LOG_LEVEL_INFO);
        LogComponentEnable ("LteUeNetDevice",LOG_LEVEL_INFO);
        LogComponentEnable ("Address", LOG_LEVEL_INFO);
        LogComponentEnable ("Application", LOG_LEVEL_INFO);
        LogComponentEnable ("ApplicationContainer", LOG_LEVEL_INFO);
        LogComponentEnable ("ConstantRateWifiManager", LOG_LEVEL_INFO);
        LogComponentEnable ("EpcHelper", LOG_LEVEL_INFO);
        LogComponentEnable ("InfrastructureWifiMac", LOG_LEVEL_INFO);
        LogComponentEnable ("InternetStackHelper", LOG_LEVEL_INFO);
        LogComponentEnable ("Ipv4AddressHelper", LOG_LEVEL_INFO);
        LogComponentEnable ("EpcEnbApplication", LOG_LEVEL_INFO);
        LogComponentEnable ("EpcSgwPgwApplication", LOG_LEVEL_INFO);
        LogComponentEnable ("EpcTft", LOG_LEVEL_INFO);
        LogComponentEnable ("InetSocketAddress", LOG_LEVEL_INFO);
        LogComponentEnable ("Ipv4Address", LOG_LEVEL_INFO);
        LogComponentEnable ("PointToPointEpcHelper", LOG_LEVEL_INFO);
        LogComponentEnable ("PointToPointHelper", LOG_LEVEL_INFO);
        LogComponentEnable ("PointToPointNetDevice", LOG_LEVEL_INFO);
        LogComponentEnable ("UdpServer", LOG_LEVEL_INFO);
        LogComponentEnable ("UdpClient", LOG_LEVEL_INFO);
        LogComponentEnable ("WifiHelper", LOG_LEVEL_INFO);
        LogComponentEnable ("WifiMac", LOG_LEVEL_INFO);
        
        CommandLine cmd;
        cmd.AddValue("simTime", "Total duration of the simulation [s])", simTime);
        cmd.Parse(argc,argv);
        ConfigStore inputConfig;
        inputConfig.ConfigureDefaults();
        Config::SetDefault ("ns3::ComponentCarrier::UlBandwidth", UintegerValue (25));// spectre ul
        Config::SetDefault ("ns3::ComponentCarrier::DlBandwidth", UintegerValue (100));// spectre dl
        Config::SetDefault ("ns3::LteEnbRrc::DefaultTransmissionMode", UintegerValue (1));//MIMO
        cmd.Parse(argc,argv);

        //creation du pgw
        Ptr<LteHelper> lteHelper = CreateObject<LteHelper> ();
        Ptr<PointToPointEpcHelper> epcHelper=CreateObject<PointToPointEpcHelper>();
        Ptr<Node>pgw=epcHelper->GetPgwNode();
        lteHelper->SetEpcHelper(epcHelper);

        //creation du serveur contenant les appli internet pouvant dialoguer avec le pgw
        NodeContainer RemoteHostContainer;
        RemoteHostContainer.Create(1);
        Ptr<Node> RemoteHost=RemoteHostContainer.Get(0);

        //Création de la pile de protocole internet
        InternetStackHelper internetLte;
        internetLte.Install (RemoteHostContainer);

        //Création d'une liaison p2p entre remotehost et pgw
        PointToPointHelper p2ph;
        p2ph.SetDeviceAttribute("DataRate", DataRateValue (DataRate("100Gbps")));
        p2ph.SetDeviceAttribute("Mtu",UintegerValue(1500));
        p2ph.SetChannelAttribute("Delay",TimeValue(Seconds(0.010)));
        NodeContainer rhp= NodeContainer(pgw,RemoteHost);
        NetDeviceContainer internetDevices=p2ph.Install(rhp);
        Ipv4AddressHelper ipv4h;//ipv4h est une addresse
        ipv4h.SetBase ("10.0.0.0","255.0.0.0");
        Ipv4InterfaceContainer internetIpfaces=ipv4h.Assign(internetDevices);
        //Ipv4Address RemoteHostAddr = internetIpfaces.GetAddress(1);//intefrace 0 est un localhost et interface 1 est p2p
       
         //Définition du routage
        Ipv4StaticRoutingHelper ipv4RoutingHelper;
        Ptr<Ipv4StaticRouting> remoteHostStaticRouting=ipv4RoutingHelper.GetStaticRouting(RemoteHost->GetObject<Ipv4>());/* recupération de addresse ipv4 du remoteHost*/
        remoteHostStaticRouting->AddNetworkRouteTo (Ipv4Address("7.0.0.0"),Ipv4Mask("255.255.255.0"),1);

        //creation de l'enb et de l'ue
        NodeContainer enbNodes;
        enbNodes.Create(1);
        Ptr<Node> enbNode = enbNodes.Get (0);
        NodeContainer ueNodes;
        ueNodes.Create(1);

        //Gestion de la mobitlité
        MobilityHelper mobility;
        mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel");
        mobility.Install(RemoteHost);
        mobility.Install(pgw);
        mobility.Install(enbNodes);
        mobility.Install(ueNodes);

        //creéation et installation des devicescards dans l'ue et dans l'enb
        NetDeviceContainer enbLteDevs;
        enbLteDevs= lteHelper->InstallEnbDevice (enbNodes);
        NetDeviceContainer ueLteDevs;
        ueLteDevs= lteHelper->InstallUeDevice (ueNodes);
        
        // Installation de la pile Ip dans l'ue
        internetLte.Install (ueNodes);
        Ipv4InterfaceContainer ueIpIface;
        ueIpIface = epcHelper->AssignUeIpv4Address (NetDeviceContainer(ueLteDevs));
        //assignation d'une adressse ip à l'ue
        Ptr<Node> ueNode = ueNodes.Get (0);

        // definintion d'une passerelle par defaut pour l'ue
        Ptr<Ipv4StaticRouting> ueStaticRouting = ipv4RoutingHelper.GetStaticRouting (ueNode->GetObject<Ipv4> ());
        ueStaticRouting->SetDefaultRoute (epcHelper->GetUeDefaultGatewayAddress (), 1);

        //Attachement de l'ue à l'enb
        lteHelper-> Attach (ueLteDevs.Get(0),enbLteDevs.Get(0));
        
        //installation des applis en lte
        protocole=17;
        appli1(onOffApp_lte ,sinkApps_lte ,RemoteHost,ueNode,ueIpIface.GetAddress (0));
        protocole=6;
        appli2(onOffApp_lte1 ,sinkApps_lte1 ,RemoteHost,ueNode,ueIpIface.GetAddress (0));
        appli3(onOffApp_lte2 ,sinkApps_lte2 ,RemoteHost,ueNode,ueIpIface.GetAddress (0));
 
      
//Implémentation du wifi

        //Création des noeuds
        NodeContainer networkNodes;
        networkNodes.Create (1);
        Ptr<Node> WifiAp = networkNodes.Get (0);
        
        MobilityHelper mobility1; 
        mobility1.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
        mobility1.Install( WifiAp);      

        //Création et implémentation d'un standard
        WifiHelper Wifi;
        Wifi.SetStandard(WIFI_PHY_STANDARD_80211ac);
        Wifi.SetRemoteStationManager("ns3::ConstantRateWifiManager",
                                     "DataMode",StringValue("VhtMcs9"),
                                     "ControlMode",StringValue("VhtMcs9"));

        //Définition du canal
        YansWifiChannelHelper WifiChannel;
        WifiChannel.SetPropagationDelay("ns3::ConstantSpeedPropagationDelayModel");
        WifiChannel.AddPropagationLoss("ns3::FixedRssLossModel","Rss",DoubleValue(1.0));
        
        //Définition des couches physiques et Mac
        YansWifiPhyHelper WifiPhy=YansWifiPhyHelper::Default();
        WifiPhy.SetChannel(WifiChannel.Create());
        WifiMacHelper WifiMac=WifiMacHelper();

        //Création et installation des devicescards du wifiAP et de la station wifi
        Ssid ssid=Ssid ("ns3-80211ac");
        WifiMac.SetType ("ns3::StaWifiMac","Ssid",SsidValue(ssid),"ActiveProbing",BooleanValue(false));
        NetDeviceContainer devicesta=Wifi.Install(WifiPhy,WifiMac,ueNode);
        WifiMac.SetType ("ns3::ApWifiMac","Ssid",SsidValue(ssid));
        NetDeviceContainer deviceap;
        deviceap=Wifi.Install(WifiPhy,WifiMac,WifiAp);

        //installation de la pile de protocole internet
        internetLte.Install (networkNodes);

        //PointToPoint Lte-Wifi
        p2ph.SetDeviceAttribute ("DataRate", StringValue ("1000Kbps"));
        p2ph.SetChannelAttribute ("Delay", StringValue ("4ms"));
        NodeContainer pwap= NodeContainer(pgw,WifiAp);
        NetDeviceContainer pgwap=p2ph.Install(pwap);

       //definition des addresses IP
        Ipv4AddressHelper address;
        address.SetBase("10.1.0.0","255.255.255.0");
        Ipv4InterfaceContainer p2pInterfacespgwwap;
        p2pInterfacespgwwap=address.Assign(pgwap);

        Ipv4InterfaceContainer wifiInterfacesap;
        wifiInterfacesap=address.Assign(deviceap);
        Ipv4InterfaceContainer wifiInterfacessta;
        wifiInterfacessta=address.Assign(devicesta);      

        //Définition du routage
        Ipv4StaticRoutingHelper ipv4RoutingHelper1,ipv4RoutingHelper2,ipv4RoutingHelper3;
        
        Ptr<Ipv4StaticRouting> remoteHostStaticRouting1=ipv4RoutingHelper1.GetStaticRouting(RemoteHost->GetObject<Ipv4>());
        remoteHostStaticRouting1->AddHostRouteTo (Ipv4Address("10.2.0.2"),Ipv4Address("10.0.0.1"),1);

        Ptr<Ipv4StaticRouting> remoteHostStaticRouting2=ipv4RoutingHelper1.GetStaticRouting(pgw->GetObject<Ipv4>());
        remoteHostStaticRouting2->AddHostRouteTo (Ipv4Address("10.2.0.2"),Ipv4Address("10.1.0.2"),2);

        Ptr<Ipv4StaticRouting> remoteHostStaticRouting3=ipv4RoutingHelper1.GetStaticRouting(WifiAp->GetObject<Ipv4>());
        remoteHostStaticRouting3->AddHostRouteTo (Ipv4Address("10.2.0.2"),Ipv4Address("10.2.0.1"),1);
        
        Ptr<Ipv4StaticRouting> remoteHostStaticRouting4=ipv4RoutingHelper1.GetStaticRouting(WifiAp->GetObject<Ipv4>());
        remoteHostStaticRouting4->AddHostRouteTo (Ipv4Address("10.2.0.2"),Ipv4Address("10.2.0.2"),1);
        
        //moniteur de flux
        NodeContainer flowmon_nodes;
        flowmon_nodes.Add(ueNode);
        flowmon_nodes.Add(RemoteHost);
        flowmon_nodes.Add(enbNode);
        
        Ptr<FlowMonitor> flowMonitor;
        FlowMonitorHelper flowHelper;
        flowMonitor=flowHelper.InstallAll();
        Simulator::Schedule(Seconds(1),&throughputMonitor,&flowHelper,flowMonitor);
        Simulator::Schedule(Seconds(2),&offload,protocol,deb,RemoteHost,ueNode, wifiInterfacessta.GetAddress (0));
        flowMonitor->SerializeToXmlFile("memoire_avant_offloading.xml",true,true);

        p2ph.EnablePcapAll("réseau-offload");
        Simulator::Stop (Seconds (10.0));

        AnimationInterface anim ("anim_memoire.xml");

        resourceId[0]=anim.AddResource ("/home/harry/ns3/ns-allinone-3.29/ns-3.29/scratch/pgw.png");
        resourceId[1]=anim.AddResource ("/home/harry/ns3/ns-allinone-3.29/ns-3.29/scratch/internet.png");
        resourceId[2]=anim.AddResource ("/home/harry/ns3/ns-allinone-3.29/ns-3.29/scratch/enodeb.png");
        resourceId[3]=anim.AddResource ("/home/harry/ns3/ns-allinone-3.29/ns-3.29/scratch/ue.png");
        resourceId[4]=anim.AddResource ("/home/harry/ns3/ns-allinone-3.29/ns-3.29/scratch/wap.png");

        anim.SetConstantPosition (pgw, 18.0, 29.3);
        anim.UpdateNodeDescription (pgw, "pgw");
        anim.UpdateNodeColor (pgw, 255, 0, 0);//rouge
        anim.UpdateNodeImage(0,resourceId[0]);

        anim.SetConstantPosition (RemoteHost, 0.0, 29.3);
        anim.UpdateNodeDescription (RemoteHost, "Internet");
        anim.UpdateNodeColor (RemoteHost, 0, 255, 0);//vert
        anim.UpdateNodeImage(1,resourceId[1]);

        anim.SetConstantPosition (WifiAp, 58.5, 45.0);
        anim.UpdateNodeDescription (WifiAp, "Point d'accès WiFi");
        anim.UpdateNodeColor (WifiAp, 0, 0, 255);//bleu
        anim.UpdateNodeImage(4,resourceId[4]);

        anim.SetConstantPosition (enbNode, 58.5,15.0);
        anim.UpdateNodeDescription (enbNode, "EnodeB");
        anim.UpdateNodeColor (enbNode, 0, 255, 255);
        anim.UpdateNodeImage(2,resourceId[2]);

        anim.SetConstantPosition (ueNode, 64.5,29.3);
        anim.UpdateNodeDescription (ueNode, "terminal");
        anim.UpdateNodeColor (ueNode, 255, 0, 255);
        anim.UpdateNodeImage(3,resourceId[3]);
        
        anim.SetStartTime(Seconds(1.8));
        anim.SetStopTime(Seconds(3));

        lteHelper->EnablePhyTraces();
        lteHelper->EnableMacTraces();
        lteHelper->EnableRlcTraces();
        lteHelper->EnablePdcpTraces();

        NS_LOG_INFO("run Simulation");

  Simulator::Run ();
         throughputMonitor (&flowHelper, flowMonitor);
        flowMonitor->SerializeToXmlFile("memoire.xml",true,true);
        recapitulatif_lte( info_lte,info_wifi,10,3,1);

  Simulator::Destroy ();
  return 0;
}
