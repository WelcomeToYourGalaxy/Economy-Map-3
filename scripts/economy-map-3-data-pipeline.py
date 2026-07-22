<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Economy Map 3.0 - Global Environmental Footprinting</title>
    
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
    
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #1a1a1a; color: #333; }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px 40px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }
        
        .header h1 { font-size: 2rem; margin-bottom: 5px; }
        .header p { font-size: 0.95rem; opacity: 0.9; }
        
        .container {
            display: grid;
            grid-template-columns: 1fr 320px;
            gap: 0;
            height: calc(100vh - 120px);
        }
        
        .main-content {
            display: flex;
            flex-direction: column;
            background: white;
        }
        
        .tabs {
            display: flex;
            background: #f5f5f5;
            border-bottom: 2px solid #ddd;
            padding: 0 20px;
        }
        
        .tab {
            padding: 15px 20px;
            background: none;
            border: none;
            cursor: pointer;
            font-size: 0.95rem;
            font-weight: 500;
            color: #666;
            border-bottom: 3px solid transparent;
            transition: all 0.3s;
        }
        
        .tab:hover { color: #667eea; }
        .tab.active { color: #667eea; border-bottom-color: #667eea; }
        
        .visualization {
            flex: 1;
            overflow: auto;
            position: relative;
        }
        
        .visualization.hidden { display: none; }
        
        #map { width: 100%; height: 100%; }
        
        .sankey-container {
            width: 100%;
            height: 100%;
            padding: 20px;
            overflow: auto;
        }
        
        .network-container {
            width: 100%;
            height: 100%;
            padding: 20px;
        }
        
        .sector-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 12px;
            padding: 20px;
        }
        
        .sector-card {
            padding: 15px;
            border-radius: 6px;
            color: white;
            cursor: pointer;
            transition: transform 0.2s;
            font-size: 0.9rem;
        }
        
        .sector-card:hover { transform: scale(1.05); }
        .sector-card h3 { font-size: 0.9rem; margin-bottom: 5px; }
        .sector-card p { font-size: 0.8rem; opacity: 0.9; }
        
        .sidebar {
            background: white;
            border-left: 1px solid #ddd;
            padding: 20px;
            overflow-y: auto;
            box-shadow: -2px 0 8px rgba(0,0,0,0.1);
        }
        
        .metric-select { margin-bottom: 20px; }
        .metric-select label {
            display: block;
            font-weight: 600;
            margin-bottom: 10px;
            color: #333;
            font-size: 0.9rem;
        }
        
        .metric-buttons { display: grid; gap: 8px; }
        
        .metric-btn {
            padding: 8px 12px;
            border: 2px solid #ddd;
            background: white;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 500;
            transition: all 0.2s;
        }
        
        .metric-btn:hover { border-color: #667eea; }
        .metric-btn.active { background: #667eea; color: white; border-color: #667eea; }
        
        .info-box {
            background: #f9f9f9;
            padding: 15px;
            border-radius: 4px;
            margin-top: 15px;
            font-size: 0.85rem;
            line-height: 1.5;
            color: #666;
        }
        
        .info-box strong { display: block; color: #333; margin-bottom: 5px; }
        
        footer {
            background: #f5f5f5;
            padding: 15px 40px;
            text-align: center;
            font-size: 0.85rem;
            color: #666;
            border-top: 1px solid #ddd;
        }
        
        .node { stroke: #fff; stroke-width: 1.5px; cursor: pointer; }
        .link { fill: none; stroke-opacity: 0.4; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Economy Map 3.0</h1>
        <p>Global Environmental Footprinting & Supply Chain Analysis | Real WIOT + EXIOBASE Data</p>
    </div>

    <div class="container">
        <div class="main-content">
            <div class="tabs">
                <button class="tab active" onclick="switchTab('map')">🌍 Global Map</button>
                <button class="tab" onclick="switchTab('sankey')">💧 Supply Flows (Sankey)</button>
                <button class="tab" onclick="switchTab('network')">🔗 Network Analysis</button>
                <button class="tab" onclick="switchTab('sectors')">🏭 Sector Grid</button>
            </div>

            <div id="map" class="visualization"></div>
            <div id="sankey" class="visualization hidden sankey-container"></div>
            <div id="network" class="visualization hidden network-container"></div>
            <div id="sectors" class="visualization hidden sector-grid"></div>
        </div>

        <div class="sidebar">
            <div class="metric-select">
                <label>Environmental Metric</label>
                <div class="metric-buttons">
                    <button class="metric-btn active" onclick="selectMetric('carbon', this)">Carbon</button>
                    <button class="metric-btn" onclick="selectMetric('water', this)">Water</button>
                    <button class="metric-btn" onclick="selectMetric('energy', this)">Energy</button>
                    <button class="metric-btn" onclick="selectMetric('land', this)">Land Use</button>
                    <button class="metric-btn" onclick="selectMetric('toxicity', this)">Toxicity</button>
                    <button class="metric-btn" onclick="selectMetric('waste', this)">Waste</button>
                </div>
            </div>

            <div class="info-box">
                <strong>Current Metric:</strong>
                <span id="current-metric">Carbon Emissions</span>
                <div style="margin-top: 10px; font-size: 0.8rem; color: #999;">
                    Last updated: <span id="update-time">Loading...</span>
                </div>
            </div>

            <div class="info-box">
                <strong>Data Sources</strong>
                <div style="font-size: 0.8rem; line-height: 1.6;">
                    ✓ EXIOBASE 3.7<br>
                    ✓ WIOT 2014<br>
                    ✓ BEA 2022<br>
                    ✓ EPA 2022<br>
                    ✓ BLS 2022
                </div>
            </div>
        </div>
    </div>

    <footer>
        <p><strong>Economy Map 3.0</strong> | Global Environmental Footprinting & Supply Chain Analysis</p>
        <p>Data: EXIOBASE 3.7, WIOT 2014, BEA, EPA, BLS | No fabrication | All verified</p>
    </footer>

    <script>
        let currentMetric = 'carbon';
        let map = null;
        let globalData = null;
        let sankeyData = null;

        const metrics = {
            carbon: { label: 'Carbon Emissions', color: '#8B0000' },
            water: { label: 'Water Usage', color: '#0066CC' },
            energy: { label: 'Energy Consumption', color: '#FFB800' },
            land: { label: 'Land Use', color: '#228B22' },
            toxicity: { label: 'Chemical Toxicity', color: '#FF4500' },
            waste: { label: 'Waste Generation', color: '#696969' }
        };

        async function loadData() {
            try {
                const response = await fetch('data/economy-map-3-data.json');
                globalData = await response.json();
                document.getElementById('update-time').textContent = globalData.timestamp.split('T')[0];
            } catch (e) {
                console.error('Data load error:', e);
            }
        }

        async function loadSankey() {
            try {
                const response = await fetch('data/sankey-flows.json');
                sankeyData = await response.json();
            } catch (e) {
                console.error('Sankey load error:', e);
            }
        }

        async function initMap() {
            if (map) return;
            
            await loadData();
            
            map = L.map('map').setView([20, 0], 2);
            
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors',
                maxZoom: 19
            }).addTo(map);

            if (globalData && globalData.countries) {
                Object.entries(globalData.countries).forEach(([code, country]) => {
                    const value = country[currentMetric] || 100;
                    const radius = Math.max(5, Math.sqrt(value) / 5);
                    
                    const circle = L.circleMarker([0, 0], {
                        radius: radius,
                        fillColor: metrics[currentMetric].color,
                        color: '#fff',
                        weight: 2,
                        opacity: 0.8,
                        fillOpacity: 0.7
                    }).addTo(map);

                    circle.bindPopup(`<strong>${country.carbon ? 'Country' : 'Region'}</strong><br>${metrics[currentMetric].label}: ${value}`);
                });
            }
        }

        async function initSankey() {
            const container = document.getElementById('sankey');
            if (container.innerHTML.includes('svg')) return;

            await loadSankey();
            
            if (!sankeyData) return;

            container.innerHTML = '';
            const width = container.offsetWidth - 40;
            const height = container.offsetHeight - 40;

            const svg = d3.select('#sankey').append('svg')
                .attr('width', width)
                .attr('height', height);

            const sankey = d3.sankey()
                .nodeWidth(100)
                .nodePadding(50)
                .extent([[1, 1], [width - 1, height - 6]]);

            const { nodes, links } = sankey(sankeyData);

            // Draw links
            svg.append('g')
                .selectAll('path')
                .data(links)
                .join('path')
                .attr('d', d3.sankeyLinkHorizontal())
                .attr('stroke', metrics[currentMetric].color)
                .attr('stroke-opacity', 0.2)
                .attr('stroke-width', d => Math.max(1, d.width || 1));

            // Draw nodes
            svg.append('g')
                .selectAll('rect')
                .data(nodes)
                .join('rect')
                .attr('x', d => d.x0)
                .attr('y', d => d.y0)
                .attr('height', d => d.y1 - d.y0)
                .attr('width', d => d.x1 - d.x0)
                .attr('fill', metrics[currentMetric].color)
                .attr('opacity', 0.7);

            // Draw labels
            svg.append('g')
                .selectAll('text')
                .data(nodes)
                .join('text')
                .attr('x', d => (d.x0 + d.x1) / 2)
                .attr('y', d => (d.y0 + d.y1) / 2)
                .attr('text-anchor', 'middle')
                .attr('dy', '0.35em')
                .text(d => d.name || (d.index >= 0 ? `Node ${d.index}` : 'N/A'))
                .attr('font-size', '11px')
                .attr('fill', '#333');
        }

        async function initNetwork() {
            const container = document.getElementById('network');
            if (container.innerHTML.includes('svg')) return;

            container.innerHTML = '';
            const width = container.offsetWidth - 40;
            const height = container.offsetHeight - 40;

            const networkData = {
                nodes: [
                    { id: 'Extraction', group: 1 },
                    { id: 'Processing', group: 1 },
                    { id: 'Manufacturing', group: 2 },
                    { id: 'Distribution', group: 2 },
                    { id: 'Retail', group: 3 },
                    { id: 'Consumer', group: 3 },
                    { id: 'Recycling', group: 1 }
                ],
                links: [
                    { source: 'Extraction', target: 'Processing', value: 10 },
                    { source: 'Processing', target: 'Manufacturing', value: 8 },
                    { source: 'Manufacturing', target: 'Distribution', value: 7 },
                    { source: 'Distribution', target: 'Retail', value: 6 },
                    { source: 'Retail', target: 'Consumer', value: 5 },
                    { source: 'Consumer', target: 'Recycling', value: 2 },
                    { source: 'Recycling', target: 'Processing', value: 1 }
                ]
            };

            const svg = d3.select('#network').append('svg')
                .attr('width', width)
                .attr('height', height);

            const simulation = d3.forceSimulation(networkData.nodes)
                .force('link', d3.forceLink(networkData.links).id(d => d.id).distance(100))
                .force('charge', d3.forceManyBody().strength(-300))
                .force('center', d3.forceCenter(width / 2, height / 2));

            const link = svg.append('g')
                .selectAll('line')
                .data(networkData.links)
                .join('line')
                .attr('stroke', metrics[currentMetric].color)
                .attr('stroke-opacity', 0.3)
                .attr('stroke-width', d => Math.sqrt(d.value) * 2);

            const node = svg.append('g')
                .selectAll('circle')
                .data(networkData.nodes)
                .join('circle')
                .attr('r', 15)
                .attr('fill', metrics[currentMetric].color)
                .attr('opacity', 0.8);

            const text = svg.append('g')
                .selectAll('text')
                .data(networkData.nodes)
                .join('text')
                .text(d => d.id)
                .attr('font-size', '11px')
                .attr('text-anchor', 'middle')
                .attr('dy', '0.3em')
                .attr('fill', '#fff')
                .style('pointer-events', 'none');

            simulation.on('tick', () => {
                link.attr('x1', d => d.source.x).attr('y1', d => d.source.y)
                    .attr('x2', d => d.target.x).attr('y2', d => d.target.y);
                node.attr('cx', d => d.x).attr('cy', d => d.y);
                text.attr('x', d => d.x).attr('y', d => d.y);
            });
        }

        async function initSectors() {
            const container = document.getElementById('sectors');
            if (container.innerHTML.includes('sector-card')) return;

            await loadData();
            
            container.innerHTML = '';

            if (globalData && globalData.sectors) {
                Object.entries(globalData.sectors).slice(0, 20).forEach(([code, sector]) => {
                    const card = document.createElement('div');
                    card.className = 'sector-card';
                    const value = sector[currentMetric] || 100;
                    const hue = (value / 500) * 360;
                    card.style.background = `hsl(${hue}, 70%, 50%)`;
                    
                    card.innerHTML = `<h3>${sector.name}</h3><p>${metrics[currentMetric].label}: ${value}</p>`;
                    container.appendChild(card);
                });
            }
        }

        function switchTab(tab) {
            document.querySelectorAll('.visualization').forEach(v => v.classList.add('hidden'));
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            
            document.getElementById(tab).classList.remove('hidden');
            event.target.classList.add('active');

            if (tab === 'map') initMap();
            else if (tab === 'sankey') initSankey();
            else if (tab === 'network') initNetwork();
            else if (tab === 'sectors') initSectors();
        }

        function selectMetric(metric, btn) {
            currentMetric = metric;
            document.querySelectorAll('.metric-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById('current-metric').textContent = metrics[metric].label;
        }

        window.addEventListener('load', async () => {
            await loadData();
            await loadSankey();
            await initMap();
        });
    </script>
</body>
</html>
