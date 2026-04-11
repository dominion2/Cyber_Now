```mermaid
graph TD
    %% Main Collection Node
    Root["This stuff is crazy"]

    %% Relationship Categories
    IP_Rel{Ip addresses}
    URL_Rel{Urls}

    %% Main Connections
    Root --> IP_Rel
    Root --> URL_Rel

    %% IP Address Nodes (Color-coded)
    IP_Rel --> IP1["116.203.80.157 (DE)"]
    IP_Rel --> IP2["134.70.96.3 (KR)"]
    IP_Rel --> IP3["167.235.109.63 (DE)"]
    IP_Rel --> IP4["85.17.65.238 (NL)"]

    %% URL Nodes
    URL_Rel --> U1["URL: 3bc6..."]
    URL_Rel --> U2["URL: abf2..."]
    URL_Rel --> U3["URL: bf3a..."]
    URL_Rel --> U4["URL: c295..."]
    URL_Rel --> U5["URL: c31c..."]
    URL_Rel --> U6["URL: e42b..."]
    URL_Rel --> U7["URL: e4ff..."]
    URL_Rel --> U8["URL: e74d..."]

    %% --- STYLING ---
    style Root fill:#f96,stroke:#333,stroke-width:2px
    style IP_Rel fill:#d1e2ff,stroke:#333
    style URL_Rel fill:#d1e2ff,stroke:#333

    classDef malicious fill:#ffcccc,stroke:#cc0000,stroke-width:2px;
    class IP1,IP4,U1,U2,U3,U4,U5,U6,U7,U8 malicious;

    classDef clean fill:#ccffcc,stroke:#006600,stroke-width:2px;
    class IP2,IP3 clean;
