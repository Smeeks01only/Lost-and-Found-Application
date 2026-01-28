```javascript
import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ScrollView, Alert } from 'react-native';
import api from '../../services/api';
import { useRouter } from 'expo-router';

import { useAuth } from '../../context/AuthContext';

export default function ReportScreen() {
    const { user } = useAuth();
    const [type, setType] = useState<'LOST' | 'FOUND'>('LOST');
    const [description, setDescription] = useState('');
    const [location, setLocation] = useState('');
    const [contact, setContact] = useState('');

    // Security Question fields (only for FOUND)
    const [secQuestion, setSecQuestion] = useState('');
    const [secAnswer, setSecAnswer] = useState('');

    const [loading, setLoading] = useState(false);
    const router = useRouter();

    const handleSubmit = async () => {
        if (!description || !location) {
            Alert.alert('Missing Info', 'Description and Location are required.');
            return;
        }

        if (type === 'FOUND' && (!secQuestion || !secAnswer)) {
            Alert.alert('Security', 'Found items match require a Security Question & Answer.');
            return;
        }

        setLoading(true);
        const payload: any = {
            description,
            location,
            date_lost_found: new Date().toISOString(),
            contact_info: contact
        };

        if (type === 'FOUND') {
            payload.security_question = secQuestion;
            payload.security_answer = secAnswer;
        }

        try {
            const endpoint = type === 'LOST' ? '/items/lost/' : '/items/found/';
            await api.post(endpoint, payload);
            Alert.alert('Success', 'Item Reported!');
            setDescription('');
            setLocation('');
            setContact('');
            router.push('/(tabs)');
        } catch (e) {
            console.log(e);
            Alert.alert('Error', 'Failed to report item.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <ScrollView contentContainerStyle={styles.container}>
            <Text style={styles.header}>Report an Item</Text>

            <View style={styles.typeContainer}>
                <TouchableOpacity
                    style={[styles.typeButton, type === 'LOST' && styles.activeType]}
                    onPress={() => setType('LOST')}
                >
                    <Text style={[styles.typeText, type === 'LOST' && styles.activeTypeText]}>I LOST something</Text>
                </TouchableOpacity>

                {user?.role !== 'LOSER' && (
                    <TouchableOpacity
                        style={[styles.typeButton, type === 'FOUND' && styles.activeTypeMatch]}
                        onPress={() => setType('FOUND')}
                    >
                        <Text style={[styles.typeText, type === 'FOUND' && styles.activeTypeText]}>I FOUND something</Text>
                    </TouchableOpacity>
                )}
            </View>

            <Text style={styles.label}>Description</Text>
            <TextInput style={styles.input} multiline value={description} onChangeText={setDescription} placeholder="e.g. Silver Laptop" />

            <Text style={styles.label}>Location</Text>
            <TextInput style={styles.input} value={location} onChangeText={setLocation} placeholder="e.g. Library" />

            <Text style={styles.label}>Contact Info</Text>
            <TextInput style={styles.input} value={contact} onChangeText={setContact} placeholder="Email or Phone" />

            {type === 'FOUND' && (
                <View style={styles.securityBox}>
                    <Text style={styles.securityTitle}>🔒 Security Check</Text>
                    <Text style={styles.securityDesc}>To prevent fraud, create a question the owner must answer.</Text>

                    <Text style={styles.label}>Question</Text>
                    <TextInput style={styles.input} value={secQuestion} onChangeText={setSecQuestion} placeholder="e.g. What is the wallpaper?" />

                    <Text style={styles.label}>Answer (Secret)</Text>
                    <TextInput style={styles.input} value={secAnswer} onChangeText={setSecAnswer} placeholder="e.g. Blue Ocean" secureTextEntry />
                </View>
            )}

            <TouchableOpacity style={styles.submitBtn} onPress={handleSubmit} disabled={loading}>
                <Text style={styles.submitText}>{loading ? 'Submitting...' : 'Submit Report'}</Text>
            </TouchableOpacity>
        </ScrollView>
    );
}

const styles = StyleSheet.create({
    container: { padding: 20, backgroundColor: '#fff', flexGrow: 1 },
    header: { fontSize: 24, fontWeight: 'bold', textAlign: 'center', marginBottom: 20 },
    typeContainer: { flexDirection: 'row', marginBottom: 20 },
    typeButton: { flex: 1, padding: 15, borderWidth: 1, borderColor: '#ddd', alignItems: 'center', borderRadius: 8, marginHorizontal: 5 },
    activeType: { backgroundColor: '#ffeebb', borderColor: '#ffa500' },
    activeTypeMatch: { backgroundColor: '#ccffcc', borderColor: '#28a745' },
    typeText: { fontWeight: '600' },
    activeTypeText: { color: '#000' },
    label: { fontSize: 16, marginBottom: 5, color: '#333' },
    input: { borderWidth: 1, borderColor: '#ccc', borderRadius: 8, padding: 12, marginBottom: 15, fontSize: 16 },
    submitBtn: { backgroundColor: '#007AFF', padding: 15, borderRadius: 10, alignItems: 'center', marginTop: 10 },
    submitText: { color: '#fff', fontSize: 18, fontWeight: 'bold' },
    securityBox: { backgroundColor: '#f0f8ff', padding: 15, borderRadius: 10, marginBottom: 20, borderWidth: 1, borderColor: '#b0c4de' },
    securityTitle: { fontWeight: 'bold', marginBottom: 5 },
    securityDesc: { fontSize: 12, color: '#666', marginBottom: 10 }
});
