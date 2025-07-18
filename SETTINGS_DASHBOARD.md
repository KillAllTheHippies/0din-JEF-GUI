# Settings Dashboard

The ChatGPT Archive Search Tool now includes a comprehensive settings dashboard that allows you to configure all aspects of the application through a user-friendly web interface.

## 🎯 Features

### 📁 Archive Configuration
- **Root Folder Selection**: Choose the folder containing your ChatGPT conversation files
- **Path Validation**: Real-time validation of archive paths
- **Folder Browser**: Built-in folder selection interface

### 🎨 Theme Customization
- **Theme Modes**: Auto (system), Light, or Dark mode
- **Accent Colors**: Choose from predefined color schemes (Blue, Purple, Green, Orange, Red, Teal)
- **Custom Colors**: Set custom primary colors with color picker
- **Live Preview**: See theme changes in real-time

### 🔍 Search Preferences
- **Default Search Mode**: Set ALL (AND) or ANY (OR) as default
- **Case Sensitivity**: Configure default case sensitivity
- **Live Search**: Enable/disable search-as-you-type
- **Result Limits**: Set maximum number of search results

### 📂 File Explorer Settings
- **Tree Depth**: Control maximum folder depth displayed
- **Sidebar Width**: Adjust file explorer width
- **Hidden Files**: Show/hide hidden files and folders
- **Auto-Expand**: Configure tree expansion behavior

### 🛡️ JEF Integration
- **JEF Path**: Configure path to JEF framework
- **Enable/Disable**: Toggle JEF integration on/off
- **Status Monitoring**: Real-time JEF availability status

### 📤 Export Preferences
- **Default Format**: Choose default export format (CSV, JSON)
- **Path Type**: Set relative or absolute paths as default
- **Export Settings**: Backup and restore configuration

### ⚡ Performance Settings
- **Search Timeout**: Configure search operation timeouts
- **Cache Size**: Set memory cache limits
- **Server Settings**: Configure host, port, and debug mode

## 🚀 Getting Started

### Accessing Settings
1. Start the application: `python app.py`
2. Open your browser to `http://localhost:5000`
3. Click the **Settings** button in the header navigation
4. Or go directly to `http://localhost:5000/settings`

### First-Time Setup
1. **Set Archive Path**: Point to your ChatGPT conversation folder
2. **Choose Theme**: Select your preferred appearance
3. **Configure Search**: Set default search preferences
4. **Save Settings**: Click "Save Settings" to persist changes

## 🔧 Configuration Management

### Settings File
- Settings are stored in `app_settings.json`
- Automatic backup on save (`.backup` extension)
- JSON format for easy manual editing

### Import/Export
- **Export**: Download current settings as JSON file
- **Import**: Upload previously exported settings
- **Reset**: Restore all settings to defaults
- **Validation**: Automatic validation of imported settings

### API Endpoints
- `GET /api/settings` - Retrieve current settings
- `POST /api/settings` - Save new settings
- `POST /api/settings/validate` - Validate settings without saving
- `POST /api/settings/reset` - Reset to defaults
- `GET /api/settings/export` - Export settings file
- `POST /api/settings/import` - Import settings file

## 🎨 Theme System

### Built-in Themes
- **Auto**: Follows system preference
- **Light**: Clean, bright interface
- **Dark**: Easy on the eyes for low-light use

### Color Schemes
- **Blue** (Default): Professional blue tones
- **Purple**: Rich purple gradients
- **Green**: Nature-inspired greens
- **Orange**: Warm, energetic orange
- **Red**: Bold red accents
- **Teal**: Calming teal colors

### Custom Colors
- Use the color picker to set any primary color
- Automatic generation of complementary colors
- CSS variables for consistent theming

## 🔍 Search Configuration

### Search Modes
- **ALL (AND)**: Find files containing all search terms
- **ANY (OR)**: Find files containing any search term
- **Case Sensitive**: Exact case matching
- **Live Search**: Real-time search as you type

### Performance Tuning
- **Max Results**: Limit results for better performance
- **Search Timeout**: Prevent long-running searches
- **Cache Size**: Balance memory usage and speed

## 🛡️ JEF Integration Settings

### Setup
1. Download/install the JEF framework
2. Set the JEF path in settings
3. Enable JEF integration
4. Restart the application

### Features
- **Content Analysis**: Advanced text analysis capabilities
- **Security Scanning**: Detect sensitive content
- **Copyright Detection**: Identify potential copyright issues
- **Configurable Tests**: Choose which analyses to run

## 📁 File Explorer Configuration

### Tree Settings
- **Max Depth**: Prevent performance issues with deep folders
- **Hidden Files**: Control visibility of system files
- **Auto-Expand**: Set default expansion behavior

### Interface
- **Sidebar Width**: Adjust for your screen size
- **Responsive Design**: Adapts to different screen sizes

## 🔧 Advanced Configuration

### Manual Editing
Edit `app_settings.json` directly for advanced configuration:

```json
{
  "archive_path": "path/to/your/chatgpt/files",
  "theme_mode": "auto",
  "accent_color": "blue",
  "custom_primary_color": "#0d6efd",
  "default_search_mode": "ALL",
  "max_results": 100,
  "jef_path": "path/to/jef",
  "enable_jef_integration": false
}
```

### Environment Variables
Override settings with environment variables:
- `ARCHIVE_PATH`: Override archive path
- `JEF_PATH`: Override JEF path
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 5000)
- `DEBUG`: Debug mode (default: true)

## 🚨 Troubleshooting

### Common Issues

**Settings not saving**
- Check file permissions in the application directory
- Ensure `app_settings.json` is writable

**Archive path not working**
- Verify the path exists and contains `.md` files
- Check folder permissions
- Use absolute paths if relative paths fail

**JEF integration issues**
- Verify JEF path is correct
- Check JEF installation
- Review console output for error messages

**Theme not applying**
- Clear browser cache
- Check for JavaScript errors in browser console
- Try a different browser

### Validation Errors
The settings system validates all inputs:
- **Paths**: Must exist and be accessible
- **Numbers**: Must be within valid ranges
- **Colors**: Must be valid hex colors (#rrggbb)
- **Booleans**: Must be true/false

### Reset Options
If settings become corrupted:
1. Use "Reset to Defaults" button in settings
2. Delete `app_settings.json` file
3. Restart the application

## 🔄 Updates and Migration

### Version Compatibility
- Settings format is versioned for compatibility
- Automatic migration of old settings
- Backup creation before updates

### New Features
- Settings automatically include new options with defaults
- No manual migration required
- Backward compatibility maintained

## 💡 Tips and Best Practices

### Performance
- Set reasonable max results (50-200)
- Use appropriate tree depth (2-4 levels)
- Enable caching for better performance

### Organization
- Use descriptive archive folder names
- Organize conversations in subfolders
- Regular backup of settings

### Security
- Keep JEF path secure if using sensitive analysis
- Regular updates of the application
- Monitor access logs if needed

## 🤝 Contributing

To add new settings options:
1. Update `config_manager.py` with new defaults
2. Add form fields to `templates/settings.html`
3. Update validation in `ConfigManager.validate_settings()`
4. Add documentation to this file

## 📚 Related Documentation

- [Installation Guide](INSTALLATION.md)
- [Architecture Overview](ARCHITECTURE.md)
- [API Documentation](API.md)
- [JEF Integration](JEF_INTEGRATION_ADVANCED.md)
- [Deployment Guide](DEPLOYMENT.md)

---

**Made with ❤️ for the ChatGPT community**