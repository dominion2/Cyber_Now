-- BINARY POLICE FORCE V32: Final Jupyter Alignment
local bpf_p = Proto("bpf_v32", "BPF Forensic Pulse V32")

-- 1. FIELDS (State, Modal, Kurtosis, Rhythm)
local pf_state  = ProtoField.string("bpf.state", "State")
local pf_modal  = ProtoField.string("bpf.modal", "Modal")
local pf_kurt   = ProtoField.string("bpf.kurt", "Kurtosis")
local pf_rhythm = ProtoField.string("bpf.rhythm", "Rhythm")

bpf_p.fields = {pf_state, pf_modal, pf_kurt, pf_rhythm}

-- 2. PERSISTENCE (Cache to prevent negative/changing numbers)
local packet_results = {}
local flow_last_ts = {}
local tcp_payload = Field.new("tcp.payload")
local udp_payload = Field.new("udp.payload")

-- 3. MATH ENGINE (1:1 Mirror of Python get_stats)
function get_bpf_metrics(buffer)
    local len = buffer:len()
    if len < 4 then return "C", "0x00", "0.0000" end

    local counts = {}
    for i = 0, 255 do counts[i] = 0 end
    local samples, max_c, m_byte = 0, 0, 0
    local stride = (len > 1000) and 32 or 1
    
    for i = 0, len - 1, stride do
        local b = buffer(i,1):uint()
        counts[b] = counts[b] + 1
        samples = samples + 1
        if counts[b] > max_c then max_c = counts[b]; m_byte = b end
    end

    local mean = samples / 256
    local s2, s4, ent = 0, 0, 0
    for i = 0, 255 do
        local c = counts[i]
        local d = c - mean
        s2 = s2 + (d^2)
        s4 = s4 + (d^4)
        if c > 0 then
            local p = c / samples
            ent = ent - (p * math.log(p) / 0.693147)
        end
    end

    local var = s2 / 256
    local kurt = (var > 0.01) and ((s4 / 256) / (var^2) - 3) or 0.0
    local state = (ent > 7.0) and "X" or "B"
    return state, string.format("0x%02X", m_byte), string.format("%.4f", kurt)
end

-- 4. DISSECTOR (Aligned Flow Tracking)
function bpf_p.dissector(tvb, pinfo, tree)
    local p_num = pinfo.number
    
    -- ONLY calculate if this is the first time we see the packet
    if not packet_results[p_num] then
        local payload_field = tcp_payload() or udp_payload()
        local state, modal, kurt
        
        if payload_field then
            state, modal, kurt = get_bpf_metrics(payload_field().tvb:range())
        else
            state, modal, kurt = "C", "0x00", "0.0000"
        end

        -- ALIGNED FLOW KEY: Using IP-to-IP only (Just like Jupyter)
        local flow_key = tostring(pinfo.net_src) .. "->" .. tostring(pinfo.net_dst)
        local now = tonumber(pinfo.abs_ts)
        local rhythm_val = 0
        
        if flow_last_ts[flow_key] then
            rhythm_val = now - flow_last_ts[flow_key]
        else
            -- Python baseline: if first packet, rhythm is ~0.0001
            rhythm_val = 0.0001
        end
        flow_last_ts[flow_key] = now
        
        -- Store in cache
        packet_results[p_num] = {
            state = state,
            modal = modal,
            kurt = kurt,
            rhythm = string.format("%.4f", rhythm_val)
        }
    end

    -- 5. APPLY TO VIEW
    local res = packet_results[p_num]
    local t = tree:add(bpf_p, tvb, "Binary Police Force V32")
    t:add(pf_state, res.state)
    t:add(pf_modal, res.modal)
    t:add(pf_kurt, res.kurt)
    t:add(pf_rhythm, res.rhythm)

    -- SYNC THE INFO COLUMN
    pinfo.cols.info:prepend("[" .. res.state .. "|" .. res.kurt .. "|R:" .. res.rhythm .. "] ")
end

register_postdissector(bpf_p)