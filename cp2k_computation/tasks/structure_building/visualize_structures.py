#!/usr/bin/env python3
"""
visualize_structures.py
Create 3D interactive visualizations of the molecular structures for CP2K calculations.
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from ase.io import read
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Color mapping for common elements
element_colors = {
    'H': 'white',
    'B': 'salmon', 
    'C': 'gray',
    'N': 'blue',
    'O': 'red',
    'Ti': 'silver',
    'Cu': 'orange',
    'default': 'purple'
}

# Atomic radii for visualization (in Angstrom)
element_radii = {
    'H': 0.31,
    'B': 0.84,
    'C': 0.76,
    'N': 0.71,
    'O': 0.66,
    'Ti': 1.60,
    'Cu': 1.32,
    'default': 0.5
}

def create_plotly_visualization(atoms, title="Molecular Structure"):
    """Create an interactive 3D visualization using Plotly."""
    
    positions = atoms.get_positions()
    symbols = atoms.get_chemical_symbols()
    
    # Group atoms by element for better visualization
    element_data = {}
    for i, symbol in enumerate(symbols):
        if symbol not in element_data:
            element_data[symbol] = {'x': [], 'y': [], 'z': [], 'indices': []}
        element_data[symbol]['x'].append(positions[i, 0])
        element_data[symbol]['y'].append(positions[i, 1])
        element_data[symbol]['z'].append(positions[i, 2])
        element_data[symbol]['indices'].append(i)
    
    fig = go.Figure()
    
    # Add each element as a separate trace
    for element, data in element_data.items():
        color = element_colors.get(element, element_colors['default'])
        radius = element_radii.get(element, element_radii['default'])
        
        fig.add_trace(go.Scatter3d(
            x=data['x'],
            y=data['y'], 
            z=data['z'],
            mode='markers',
            marker=dict(
                size=radius * 20,  # Scale for visibility
                color=color,
                opacity=0.8,
                line=dict(width=2, color='black')
            ),
            name=f'{element} ({len(data["x"])} atoms)',
            text=[f'{element}{i}' for i in data['indices']],
            hovertemplate='<b>%{text}</b><br>' +
                         'X: %{x:.2f} Å<br>' +
                         'Y: %{y:.2f} Å<br>' +
                         'Z: %{z:.2f} Å<extra></extra>'
        ))
    
    # Calculate bonds (simple distance-based)
    bonds = []
    max_bond_length = 2.0  # Angstrom
    
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            dist = np.linalg.norm(positions[i] - positions[j])
            if dist < max_bond_length:
                bonds.append((i, j, dist))
    
    # Add bonds as lines
    for i, j, dist in bonds:
        fig.add_trace(go.Scatter3d(
            x=[positions[i, 0], positions[j, 0]],
            y=[positions[i, 1], positions[j, 1]],
            z=[positions[i, 2], positions[j, 2]],
            mode='lines',
            line=dict(color='gray', width=3),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f'{title}<br><sub>Total atoms: {len(atoms)} | Bonds shown: {len(bonds)}</sub>',
            x=0.5,
            font=dict(size=16)
        ),
        scene=dict(
            xaxis_title='X (Å)',
            yaxis_title='Y (Å)', 
            zaxis_title='Z (Å)',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            ),
            aspectmode='cube'
        ),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left", 
            x=0.01
        ),
        width=800,
        height=600
    )
    
    return fig

def create_matplotlib_visualization(atoms, title="Molecular Structure"):
    """Create a 3D visualization using Matplotlib."""
    
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    
    positions = atoms.get_positions()
    symbols = atoms.get_chemical_symbols()
    
    # Plot atoms by element
    for element in set(symbols):
        indices = [i for i, sym in enumerate(symbols) if sym == element]
        if indices:
            coords = positions[indices]
            color = element_colors.get(element, element_colors['default'])
            radius = element_radii.get(element, element_radii['default'])
            
            ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2],
                      c=color, s=radius*200, alpha=0.8, 
                      label=f'{element} ({len(indices)})', 
                      edgecolors='black', linewidth=1)
    
    # Add bonds
    max_bond_length = 2.0
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            dist = np.linalg.norm(positions[i] - positions[j])
            if dist < max_bond_length:
                ax.plot([positions[i, 0], positions[j, 0]],
                       [positions[i, 1], positions[j, 1]], 
                       [positions[i, 2], positions[j, 2]],
                       'gray', alpha=0.6, linewidth=1)
    
    ax.set_xlabel('X (Å)')
    ax.set_ylabel('Y (Å)')
    ax.set_zlabel('Z (Å)')
    ax.set_title(title)
    ax.legend()
    
    # Make axes equal
    max_range = np.array([positions[:, 0].max() - positions[:, 0].min(),
                         positions[:, 1].max() - positions[:, 1].min(),
                         positions[:, 2].max() - positions[:, 2].min()]).max() / 2.0
    mid_x = (positions[:, 0].max() + positions[:, 0].min()) * 0.5
    mid_y = (positions[:, 1].max() + positions[:, 1].min()) * 0.5
    mid_z = (positions[:, 2].max() + positions[:, 2].min()) * 0.5
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)
    
    return fig

def visualize_all_structures():
    """Create visualizations for all molecular structures."""
    
    structures = {
        'Boric Acid (B(OH)₃)': 'boric_acid.xyz',
        'Ethylene Glycol (Diol)': 'ethylene_glycol.xyz', 
        'Formylbenzoate Anion': 'formylbenzoate.xyz',
        'BOC Complex (Boronate + Diol)': 'boc_complex.xyz',
        'Slab + Pentamer System': 'slab_pentamer.xyz'
    }
    
    print("🧬 Creating 3D molecular visualizations...")
    print("=" * 50)
    
    # Create Plotly visualizations (interactive)
    for name, filename in structures.items():
        try:
            atoms = read(filename)
            print(f"📊 {name}: {len(atoms)} atoms")
            
            # Create interactive Plotly visualization
            fig = create_plotly_visualization(atoms, name)
            html_filename = filename.replace('.xyz', '_interactive.html')
            fig.write_html(html_filename)
            print(f"   ✅ Interactive plot saved: {html_filename}")
            
            # Create static matplotlib visualization
            fig_mpl = create_matplotlib_visualization(atoms, name)
            png_filename = filename.replace('.xyz', '_static.png')
            fig_mpl.savefig(png_filename, dpi=300, bbox_inches='tight')
            plt.close(fig_mpl)
            print(f"   ✅ Static plot saved: {png_filename}")
            
        except Exception as e:
            print(f"   ❌ Error with {filename}: {e}")
    
    print("\n🎉 Visualization complete!")
    print("\nFiles created:")
    print("📱 Interactive HTML files (open in browser for 3D interaction)")
    print("🖼️  Static PNG files (high-resolution images)")
    
    # Create a summary HTML file
    create_summary_html(structures)

def create_summary_html(structures):
    """Create a summary HTML file with all visualizations."""
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CP2K Molecular Structure Visualizations</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .structure { margin: 30px 0; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }
            .structure h2 { color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }
            .links { margin: 10px 0; }
            .links a { 
                display: inline-block; 
                margin: 5px 10px 5px 0; 
                padding: 8px 16px; 
                background-color: #4CAF50; 
                color: white; 
                text-decoration: none; 
                border-radius: 4px; 
            }
            .links a:hover { background-color: #45a049; }
            .info { color: #666; font-style: italic; margin: 10px 0; }
        </style>
    </head>
    <body>
        <h1>🧬 CP2K Molecular Structure Visualizations</h1>
        <p>This page provides access to 3D visualizations of all molecular structures used in the CP2K calculations.</p>
    """
    
    for name, filename in structures.items():
        try:
            atoms = read(filename)
            html_file = filename.replace('.xyz', '_interactive.html')
            png_file = filename.replace('.xyz', '_static.png')
            
            html_content += f"""
            <div class="structure">
                <h2>{name}</h2>
                <div class="info">
                    Atoms: {len(atoms)} | Formula: {atoms.get_chemical_formula()} | File: {filename}
                </div>
                <div class="links">
                    <a href="{html_file}" target="_blank">🌐 Interactive 3D View</a>
                    <a href="{png_file}" target="_blank">🖼️ Static Image</a>
                    <a href="{filename}" target="_blank">📄 XYZ File</a>
                </div>
            </div>
            """
        except:
            continue
    
    html_content += """
        <div style="margin-top: 40px; padding: 20px; background-color: #f0f0f0; border-radius: 8px;">
            <h3>📝 Notes</h3>
            <ul>
                <li><strong>Interactive views</strong>: Click and drag to rotate, scroll to zoom, hover for atom info</li>
                <li><strong>Color scheme</strong>: H=white, C=gray, O=red, B=salmon, Ti=silver</li>
                <li><strong>Bonds</strong>: Shown for atoms within 2.0 Å distance</li>
                <li><strong>File formats</strong>: HTML for interaction, PNG for publication</li>
            </ul>
        </div>
    </body>
    </html>
    """
    
    with open('visualizations_summary.html', 'w') as f:
        f.write(html_content)
    
    print("📋 Summary page created: visualizations_summary.html")

if __name__ == "__main__":
    # Install required packages if not available
    try:
        import plotly
    except ImportError:
        print("Installing plotly for interactive visualizations...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'plotly'])
        import plotly.graph_objects as go
    
    visualize_all_structures() 