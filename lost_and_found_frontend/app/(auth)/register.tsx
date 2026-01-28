import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ActivityIndicator, Alert } from 'react-native';
import { useRouter } from 'expo-router';
import { register } from '../../services/auth';

export default function RegisterScreen() {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [role, setRole] = useState('LOSER');
    const [loading, setLoading] = useState(false);
    const router = useRouter();

    const handleRegister = async () => {
        if (!username || !password) {
            Alert.alert('Error', 'Please fill in all required fields.');
            return;
        }

        setLoading(true);
        try {
            await register(username, email, password, role);
            Alert.alert('Success', 'Account created! Please log in.');
            router.back();
        } catch (error) {
            console.log(error);
            Alert.alert('Registration Failed', 'Could not create account.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Create Account</Text>

            <TextInput
                style={styles.input}
                placeholder="Username"
                value={username}
                onChangeText={setUsername}
                autoCapitalize="none"
            />
            <TextInput
                style={styles.input}
                placeholder="Email (Optional)"
                value={email}
                onChangeText={setEmail}
                keyboardType="email-address"
                autoCapitalize="none"
            />
            <TextInput
                style={styles.input}
                placeholder="Password"
                value={password}
                onChangeText={setPassword}
                secureTextEntry
            />

            <Text style={styles.label}>Select Role:</Text>
            <View style={styles.roleContainer}>
                {['LOSER', 'OFFICE', 'TECH'].map((r) => (
                    <TouchableOpacity
                        key={r}
                        style={[styles.roleButton, role === r && styles.roleActive]}
                        onPress={() => setRole(r)}
                    >
                        <Text style={[styles.roleText, role === r && styles.roleTextActive]}>{r}</Text>
                    </TouchableOpacity>
                ))}
            </View>

            <TouchableOpacity style={styles.button} onPress={handleRegister} disabled={loading}>
                {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Sign Up</Text>}
            </TouchableOpacity>

            <TouchableOpacity style={styles.linkButton} onPress={() => router.back()}>
                <Text style={styles.linkText}>Already have an account? Log In</Text>
            </TouchableOpacity>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        padding: 20,
        backgroundColor: '#fff',
    },
    title: {
        fontSize: 28,
        fontWeight: 'bold',
        textAlign: 'center',
        marginBottom: 30,
        color: '#333',
    },
    input: {
        height: 50,
        borderColor: '#ddd',
        borderWidth: 1,
        borderRadius: 8,
        paddingHorizontal: 15,
        marginBottom: 15,
        fontSize: 16,
        backgroundColor: '#f9f9f9',
    },
    label: {
        fontSize: 16,
        marginBottom: 10,
        color: '#333',
        fontWeight: '600',
    },
    roleContainer: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginBottom: 20,
    },
    roleButton: {
        flex: 1,
        padding: 10,
        borderWidth: 1,
        borderColor: '#ddd',
        borderRadius: 8,
        alignItems: 'center',
        marginHorizontal: 5,
        backgroundColor: '#f9f9f9',
    },
    roleActive: {
        borderColor: '#007AFF',
        backgroundColor: '#e6f2ff',
    },
    roleText: {
        fontWeight: '600',
        color: '#666',
        fontSize: 12,
    },
    roleTextActive: {
        color: '#007AFF',
    },
    button: {
        backgroundColor: '#28a745',
        height: 50,
        borderRadius: 8,
        justifyContent: 'center',
        alignItems: 'center',
        marginTop: 10,
    },
    buttonText: {
        color: '#fff',
        fontSize: 18,
        fontWeight: '600',
    },
    linkButton: {
        marginTop: 20,
        alignItems: 'center',
    },
    linkText: {
        color: '#007AFF',
        fontSize: 16,
    },
});
