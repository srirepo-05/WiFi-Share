# FileFling: Cross-Device File Sharing System
## Project Overview
FileNet is a web-based file sharing system that enables users to securely share files across different devices on a local network. The system generates QR codes for easy mobile access and provides a user-friendly interface for file management.

## Key Features
1. **Secure Authentication**
   - Username/password-based login system
   - Session management for web access
   - Token-based authentication for mobile devices
   - Password hashing for security

2. **Cross-Device Compatibility**
   - Web interface accessible from any browser
   - Mobile-friendly design
   - QR code generation for quick mobile access
   - Automatic browser launch on desktop

3. **File Management**
   - Shared folder creation and management
   - File listing with size and type information
   - File download capabilities
   - Support for both files and directories

4. **System Architecture**
   - Flask-based web server
   - Local network deployment
   - Automatic IP detection
   - Graceful shutdown handling

## Technical Implementation

### Server Configuration
- Flask web server running on port 5000
- Binds to all network interfaces (0.0.0.0)
- Configurable secret key for session management
- Custom shutdown handlers for graceful termination

### Security Features
1. **Authentication System**
   ```python
   USERS = {
       'user': generate_password_hash('passkey')
   }
   ```
   - Werkzeug's security functions for password hashing
   - Session-based authentication for web users
   - UUID-based tokens for mobile access

2. **Access Control**
   - Login required decorator for protected routes
   - Token validation for mobile access
   - Secure file access paths

### File System Integration
1. **Shared Folder Management**
   - Default location: `~/Desktop/Share-Folder`
   - Automatic folder creation if not exists
   - Support for both development and compiled environments
   - Proper path handling across operating systems

2. **File Operations**
   - Size formatting (B, KB, MB)
   - File type detection
   - Secure file downloads
   - Directory structure preservation

### Network Features
1. **IP Detection**
   ```python
   def get_local_ip():
       try:
           s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
           s.connect(('8.8.8.8', 80))
           IP = s.getsockname()[0]
           s.close()
           return IP
       except Exception:
           return '127.0.0.1'
   ```
   - Automatic local IP detection
   - Fallback to localhost if detection fails
   - Socket-based IP resolution

2. **QR Code Integration**
   - Dynamic QR code generation
   - Embedded token in QR code URL
   - Base64 encoding for web display

## Routes and Endpoints

1. **Main Routes**
   - `/` - Home page with QR code
   - `/login` - Authentication page
   - `/files` - File listing
   - `/download/<filename>` - File download
   - `/logout` - Session termination
   - `/shutdown` - Server shutdown

2. **Security Middleware**
   - Login requirement validation
   - Token verification
   - Session management

## Deployment and Usage

### Setup Requirements
- Python 3.x
- Flask
- qrcode
- werkzeug
- Additional Python packages: io, base64, uuid, webbrowser, threading

### Running the Application
1. Start the application:
   ```bash
   python FileNet.py
   ```
2. Browser automatically opens to login page
3. Access shared folder at `~/Desktop/Share-Folder`
4. Use QR code for mobile access

### Error Handling
- Comprehensive try-except blocks
- Detailed error logging
- Graceful degradation
- User-friendly error messages

## Security Considerations

1. **Authentication Security**
   - Hashed password storage
   - Session-based authentication
   - Unique tokens for mobile access

2. **File System Security**
   - Restricted to designated shared folder
   - Path validation
   - File access controls

3. **Network Security**
   - Local network operation
   - Token-based access
   - Session management

## Future Enhancements
1. **Potential Improvements**
   - File upload functionality
   - User management system
   - Multiple shared folders
   - File encryption
   - Real-time file sync
   - Progress indicators for large files
   - Multiple user support

2. **Security Enhancements**
   - HTTPS support
   - File access logging
   - Advanced authentication methods
   - File integrity verification

## Conclusion
FileNet provides a secure and efficient solution for local network file sharing with cross-device compatibility. Its simple yet effective design makes it suitable for both personal and small office environments where quick file access across devices is needed.
